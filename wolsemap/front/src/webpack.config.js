const webpack = require('webpack');

const common = {
  context: __dirname,
  entry: {
    wolsemap: './wolsemap_app.js'
  },
  output: {
    path: __dirname + '/../dist',
    filename: '[name].js'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['env', 'react']
          }
        }
      },
      {test: /\.jsx$/, use: 'jsx-loader'},
      {test: /\.css$/, use: ['style-loader', 'css-loader']},
      {test: /\.scss$/, use: ['style-loader', 'css-loader', 'sass-loader']},
      {test: /\.svg$/, use: 'svg-use'},
    ]
  },
  resolve: {
    extensions: ['*', '.js', '.jsx', 'css', 'les']
  },
  optimization: {
    minimize: true
  },
  node: {
    net: 'empty',
    tls: 'empty',
    fs: 'empty'
  }
};

module.exports = common;
