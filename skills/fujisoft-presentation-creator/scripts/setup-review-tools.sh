#!/bin/bash

# FUJISOFT America Slide Template - Visual Review Tools Setup
# このスクリプトは視覚的レビューに必要な依存関係をインストールします

echo "🚀 Setting up FUJISOFT America Slide Visual Review Tools..."

# 現在のディレクトリを保存
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Node.js バージョンチェック
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v)
echo "✅ Node.js version: $NODE_VERSION"

# npm依存関係のインストール
echo "📦 Installing dependencies..."
if npm install; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# 実行権限を付与
chmod +x visual-review.js

# テスト実行
echo "🧪 Testing installation..."
if node visual-review.js --help &> /dev/null || node visual-review.js 2>&1 | grep -q "Usage:"; then
    echo "✅ Installation successful!"
    echo ""
    echo "🎯 Usage:"
    echo "  node visual-review.js <html-file-path> [output-directory]"
    echo ""
    echo "📋 Examples:"
    echo "  node visual-review.js ../template/FUJISOFT_America_Slide_Template.html"
    echo "  node visual-review.js ./my-presentation.html ./review-results"
    echo ""
    echo "📊 The tool will generate:"
    echo "  - Screenshots of each slide"
    echo "  - JSON report with detailed analysis"  
    echo "  - HTML report for easy viewing"
    echo ""
else
    echo "❌ Installation test failed"
    exit 1
fi

echo "🎉 Setup completed successfully!"