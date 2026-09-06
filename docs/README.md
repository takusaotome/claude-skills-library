# docs/ — Jekyll site

The published site is built by GitHub Pages' own builder (`build_type: legacy`,
source `main` / `/docs`). The `Docs Build` job in CI builds the same source with
this directory's `Gemfile` to catch broken Liquid, front matter, or config before
a PR merges.

## Why Gemfile.lock is committed

`Gemfile` asks for `github-pages` with no version constraint. Without a lockfile
the gem set is re-resolved on every CI run, so an upstream release can break the
build with no change on our side. That happened once: between 2026-07-07 and
2026-08-30 the resolution started producing jekyll 3.9 / liquid 4.0.3, whose
`taint_check` calls `String#tainted?` — removed in Ruby 3.2 — and `Docs Build`
failed on Ruby 3.3.

The committed lock pins the working set:

| gem | version |
|-----|---------|
| github-pages | 232 |
| jekyll | 3.10.0 |
| liquid | 4.0.4 |

jekyll 3.10.0 matches what the live site reports in its `<meta name="generator">`
tag, so CI and production agree on the Jekyll version.

The lock also carries `just-the-docs 0.10.2`, but that gem is **not** what renders
the site: `_config.yml` uses `remote_theme: just-the-docs/just-the-docs@v0.10.0`,
which Jekyll fetches from GitHub by tag at build time. The theme is therefore
outside the lock's protection, and remains an external dependency.

## Regenerating the lock

Two things matter, and only one of them is obvious.

**1. Delete the existing lock first.** With a lock present, `bundle install`
honours it and resolves nothing — you get a byte-identical file and a false sense
that you regenerated it.

**2. Use Bundler 2.3.x.** This, not the Ruby version, is what selects the working
gem set. Controlled runs:

| Ruby | Bundler | resolves to |
|------|---------|-------------|
| 3.1 | 2.3.27 | github-pages 232 / jekyll 3.10.0 / liquid 4.0.4 ✅ |
| 3.3 | 2.3.27 | github-pages 232 / jekyll 3.10.0 / liquid 4.0.4 ✅ |
| 3.1 | 2.5.22 | github-pages 222 / jekyll 3.9.0 / liquid 4.0.3 ❌ |
| 3.3 | 2.5.22 | github-pages 222 / jekyll 3.9.0 / liquid 4.0.3 ❌ |

The `ruby:3.1` image happens to ship Bundler 2.3.27, which is why pinning the
image alone appears to work — but that is incidental. If the image's bundled
Bundler ever moves to 2.5.x, the same command silently produces the broken set.
Install the Bundler version explicitly.

CI runs on `ubuntu-latest` (x86_64-linux), so generate under
`--platform linux/amd64` and add the other platforms explicitly. Without the
platform flag on Apple Silicon you get `aarch64-linux` only, and CI fails to
install.

```bash
cd docs
rm -f Gemfile.lock
docker run --rm --platform linux/amd64 -v "$PWD:/srv" -w /srv ruby:3.1 bash -lc '
  gem install bundler -v 2.3.27 --no-document -q &&
  bundle _2.3.27_ install &&
  bundle _2.3.27_ lock --add-platform arm64-darwin aarch64-linux
'
```

`--add-platform` takes a list. Repeating the flag does **not** accumulate — the
second occurrence replaces the first, and you silently end up with one platform
missing. Pass both values to a single flag.

Check that `PLATFORMS` lists `x86_64-linux`, `aarch64-linux`, and `arm64-darwin`.
`aarch64-linux` is the one Docker uses on Apple Silicon; without it, every local
build rewrites the lock. `arm64-darwin` goes unused whenever the host Ruby is too
old for these gems — macOS system Ruby is 2.6 — but it costs nothing and applies
as soon as someone runs Jekyll natively on a Mac.

Then verify under the same conditions CI uses — `ruby/setup-ruby` with
`bundler-cache: true` sets `deployment true` whenever a lock exists, so the
install is frozen and will fail rather than silently re-resolve:

```bash
docker run --rm --platform linux/amd64 -v "$PWD:/srv" -w /srv ruby:3.3 bash -lc '
  export BUNDLE_DEPLOYMENT=true
  bundle install --quiet && bundle exec jekyll build -d /tmp/site
'
rm -rf vendor
```

`export` matters. Written as `BUNDLE_DEPLOYMENT=true bundle install && bundle exec
…`, the variable applies only to `bundle install`; the gems land in
`vendor/bundle` but `bundle exec` then looks at the system gem path and fails with
`command not found: jekyll`.

Deployment mode installs gems into `docs/vendor/bundle`. That path is gitignored,
but delete it so it does not linger.

## Local preview

macOS system Ruby (2.6) is too old for these gems, so preview through Docker:

```bash
cd docs
docker run --rm -p 4000:4000 -v "$PWD:/srv" -w /srv ruby:3.1 \
  bash -lc "bundle install --quiet && bundle exec jekyll serve --host 0.0.0.0"
```

Then open <http://127.0.0.1:4000/claude-skills-library/>. The bare `/` returns
404 — that is correct, `baseurl` is `/claude-skills-library`.

This runs natively on the host architecture. That is safe because `aarch64-linux`
is in the lock's `PLATFORMS`; drop it and this command starts rewriting
`Gemfile.lock` on every preview.

## Trade-off introduced by pinning

Before the lock, CI re-resolved on every run and so tracked whatever GitHub Pages
shipped. It now stays on the pinned set. That removes the "CI breaks with no
change on our side" failure, and adds the opposite one: if GitHub upgrades its
builder, production moves and CI does not, so CI can stay green while the live
build breaks.

Nothing watches for that drift today — there is no `.github/dependabot.yml`. The
cheap check is to compare the live site's `<meta name="generator">` against the
`jekyll` version in this lock:

```bash
curl -s https://takusaotome.github.io/claude-skills-library/ | grep 'name="generator"'
grep '^    jekyll (' Gemfile.lock
```

If they diverge, regenerate the lock using the procedure above. Note that
Dependabot would not be a drop-in answer here: it runs modern Bundler, which
resolves to the broken 222 / 3.9.0 set.

## Known drift, tracked separately

- `_config.yml` `description` says "78 skills"; `skills/` holds 114 directories.
- `_config.yml` has `search.heading_level: 3` as a flat key, so it never resolves
  as `site.search.heading_level`. It needs to be nested under `search:`.
- Category card counts in `en/index.md` and `ja/index.md` no longer match the
  number of pages in each category.
- Moving off the `github-pages` gem to Jekyll 4 is tracked in issue #84. It is
  not urgent: the live site is built by GitHub, not by this Gemfile.
