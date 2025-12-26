const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

class SlideVisualReviewer {
  constructor(htmlFilePath, outputDir = './review-output') {
    this.htmlFilePath = path.resolve(htmlFilePath);
    this.outputDir = path.resolve(outputDir);
    this.issues = [];
    
    // 重要なレイアウトエリア定義
    this.reviewAreas = {
      footerZone: { y: 620, height: 100 },   // フッター部分（底部100px）
      contentZone: { y: 50, height: 570 },   // メインコンテンツエリア
      headerZone: { y: 0, height: 50 },      // ヘッダーエリア
      safeZone: { y: 50, height: 520 }       // フッターから安全な距離を保ったエリア（100px確保）
    };
    
    // Puppeteer設定
    this.puppeteerConfig = {
      viewport: { width: 1280, height: 720 },
      deviceScaleFactor: 2,
      fullPage: false
    };
  }

  async initialize() {
    // 出力ディレクトリ作成
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
    }
    
    // HTMLファイル存在確認
    if (!fs.existsSync(this.htmlFilePath)) {
      throw new Error(`HTML file not found: ${this.htmlFilePath}`);
    }
  }

  async reviewSlides() {
    await this.initialize();
    
    const browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-dev-shm-usage']
    });
    
    try {
      const page = await browser.newPage();
      await page.setViewport(this.puppeteerConfig.viewport);
      
      // HTMLファイルを開く
      const fileUrl = `file://${this.htmlFilePath}`;
      await page.goto(fileUrl, { waitUntil: 'networkidle0' });
      
      // スライド数を取得
      const slideCount = await page.evaluate(() => {
        const slides = document.querySelectorAll('section');
        return slides.length;
      });
      
      console.log(`Found ${slideCount} slides to review`);
      
      // 各スライドをレビュー
      for (let i = 0; i < slideCount; i++) {
        await this.reviewSlide(page, i + 1);
      }
      
      // レビューレポート生成
      await this.generateReport();
      
    } finally {
      await browser.close();
    }
    
    return this.issues;
  }
  
  async reviewSlide(page, slideNumber) {
    console.log(`Reviewing slide ${slideNumber}...`);
    
    // スライドに移動（MARPのナビゲーション）
    if (slideNumber > 1) {
      for (let i = 1; i < slideNumber; i++) {
        await page.keyboard.press('ArrowRight');
        await page.waitForTimeout(500);
      }
    }
    
    // スクリーンショット撮影
    const screenshotPath = path.join(this.outputDir, `slide-${slideNumber}.png`);
    await page.screenshot({
      path: screenshotPath,
      clip: { x: 0, y: 0, width: 1280, height: 720 }
    });
    
    // DOM要素分析
    const analysis = await page.evaluate((areas) => {
      const elements = Array.from(document.querySelectorAll('section.active *'));
      const footerOverlaps = [];
      const contentOverflows = [];
      
      elements.forEach((el, index) => {
        const rect = el.getBoundingClientRect();
        const tagName = el.tagName.toLowerCase();
        const content = el.textContent ? el.textContent.trim().substring(0, 50) : '';
        
        // フッターエリア（底部80px）との重複チェック
        if (rect.bottom > areas.footerZone.y && rect.top < areas.footerZone.y + areas.footerZone.height) {
          footerOverlaps.push({
            element: tagName,
            content: content,
            position: {
              top: Math.round(rect.top),
              bottom: Math.round(rect.bottom),
              left: Math.round(rect.left),
              right: Math.round(rect.right)
            },
            overlapHeight: Math.round(rect.bottom - areas.footerZone.y)
          });
        }
        
        // コンテンツがスライド境界を超えているかチェック
        if (rect.right > 1280 || rect.bottom > 720 || rect.left < 0 || rect.top < 0) {
          contentOverflows.push({
            element: tagName,
            content: content,
            position: {
              top: Math.round(rect.top),
              bottom: Math.round(rect.bottom),
              left: Math.round(rect.left),
              right: Math.round(rect.right)
            }
          });
        }
      });
      
      return { footerOverlaps, contentOverflows };
    }, this.reviewAreas);
    
    // 問題を記録
    if (analysis.footerOverlaps.length > 0) {
      this.issues.push({
        slide: slideNumber,
        type: 'footer_overlap',
        severity: 'high',
        description: 'Content overlapping with footer area',
        details: analysis.footerOverlaps,
        screenshot: screenshotPath
      });
    }
    
    if (analysis.contentOverflows.length > 0) {
      this.issues.push({
        slide: slideNumber,
        type: 'content_overflow',
        severity: 'medium',
        description: 'Content overflowing slide boundaries',
        details: analysis.contentOverflows,
        screenshot: screenshotPath
      });
    }
    
    // スライド品質スコア計算
    const qualityScore = this.calculateQualityScore(analysis);
    console.log(`Slide ${slideNumber} quality score: ${qualityScore}/100`);
    
    return analysis;
  }
  
  calculateQualityScore(analysis) {
    let score = 100;
    
    // フッター重複: -20点 per overlap
    score -= analysis.footerOverlaps.length * 20;
    
    // コンテンツオーバーフロー: -10点 per overflow
    score -= analysis.contentOverflows.length * 10;
    
    return Math.max(0, score);
  }
  
  async generateReport() {
    const reportPath = path.join(this.outputDir, 'review-report.json');
    const htmlReportPath = path.join(this.outputDir, 'review-report.html');
    
    // JSON レポート
    const report = {
      timestamp: new Date().toISOString(),
      htmlFile: this.htmlFilePath,
      totalIssues: this.issues.length,
      issuesByType: this.groupIssuesByType(),
      issues: this.issues
    };
    
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    
    // HTML レポート生成
    const htmlReport = this.generateHtmlReport(report);
    fs.writeFileSync(htmlReportPath, htmlReport);
    
    console.log(`\nReview completed!`);
    console.log(`- Total issues found: ${this.issues.length}`);
    console.log(`- Report saved to: ${reportPath}`);
    console.log(`- HTML report: ${htmlReportPath}`);
    
    if (this.issues.length > 0) {
      console.log(`\nIssues by type:`);
      Object.entries(this.groupIssuesByType()).forEach(([type, count]) => {
        console.log(`  - ${type}: ${count}`);
      });
    }
  }
  
  groupIssuesByType() {
    return this.issues.reduce((acc, issue) => {
      acc[issue.type] = (acc[issue.type] || 0) + 1;
      return acc;
    }, {});
  }
  
  generateHtmlReport(report) {
    return `
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Slide Visual Review Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, sans-serif; margin: 40px; line-height: 1.6; }
        .header { border-bottom: 2px solid #1a237e; padding-bottom: 20px; margin-bottom: 30px; }
        .summary { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 30px; }
        .issue { border: 1px solid #ddd; border-radius: 8px; margin-bottom: 20px; padding: 20px; }
        .issue.high { border-left: 4px solid #d32f2f; }
        .issue.medium { border-left: 4px solid #f57c00; }
        .issue.low { border-left: 4px solid #388e3c; }
        .screenshot { max-width: 100%; height: auto; border: 1px solid #ddd; margin-top: 10px; }
        .details { background: #fafafa; padding: 15px; margin-top: 15px; border-radius: 4px; }
        pre { overflow-x: auto; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔍 Slide Visual Review Report</h1>
        <p><strong>File:</strong> ${report.htmlFile}</p>
        <p><strong>Generated:</strong> ${new Date(report.timestamp).toLocaleString()}</p>
    </div>
    
    <div class="summary">
        <h2>📊 Summary</h2>
        <p><strong>Total Issues:</strong> ${report.totalIssues}</p>
        <ul>
            ${Object.entries(report.issuesByType).map(([type, count]) => 
              `<li><strong>${type}:</strong> ${count}</li>`
            ).join('')}
        </ul>
    </div>
    
    <div class="issues">
        <h2>🚨 Issues Found</h2>
        ${report.issues.length === 0 ? '<p>✅ No issues found! Great job!</p>' : 
          report.issues.map(issue => `
            <div class="issue ${issue.severity}">
                <h3>Slide ${issue.slide}: ${issue.description}</h3>
                <p><strong>Type:</strong> ${issue.type} | <strong>Severity:</strong> ${issue.severity}</p>
                <div class="details">
                    <strong>Details:</strong>
                    <pre>${JSON.stringify(issue.details, null, 2)}</pre>
                </div>
                <img class="screenshot" src="${path.basename(issue.screenshot)}" alt="Slide ${issue.slide} screenshot">
            </div>
          `).join('')
        }
    </div>
</body>
</html>`;
  }
}

// コマンドライン実行
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log(`
Usage: node visual-review.js <html-file-path> [output-directory]

Examples:
  node visual-review.js ./presentation.html
  node visual-review.js ./presentation.html ./review-results
    `);
    process.exit(1);
  }
  
  const htmlFile = args[0];
  const outputDir = args[1] || './review-output';
  
  try {
    const reviewer = new SlideVisualReviewer(htmlFile, outputDir);
    const issues = await reviewer.reviewSlides();
    
    process.exit(issues.length > 0 ? 1 : 0);
  } catch (error) {
    console.error('Error during visual review:', error);
    process.exit(1);
  }
}

// モジュールとして使用される場合とコマンドライン実行の場合を分ける
if (require.main === module) {
  main().catch(console.error);
}

module.exports = SlideVisualReviewer;