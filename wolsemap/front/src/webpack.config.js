const webpack = require('webpack');
const CommonsChunkPlugin = require('webpack/lib/optimize/CommonsChunkPlugin');
const UglifyJsPlugin = require('webpack/lib/optimize/UglifyJsPlugin');
const merge = require('webpack-merge');

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
    preLoaders: [
      {test: /\.json$/, loader: 'json-loader'}
    ],
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel',
        query: {
          presets: ['es2015', 'react']
        }
      },
      {test: /\.jsx$/, loader: 'jsx'},
      {test: /\.css$/, loader: 'style!css'},
      {test: /\.scss$/, loader: 'style!css!sass'},
      {test: /\.svg$/, loader: 'svg-loader'}
    ]
  },
  resolve: {
    root: __dirname,
    extensions: ['', '.js', '.jsx', 'css', 'les']
  },
  plugins: [
    new CommonsChunkPlugin({
      name: 'common',
      filename: 'commons.js',
      minChunks: 2
    }),
    new UglifyJsPlugin({
      sourceMap: false
    })
  ],
  node: {
    net: 'empty',
    tls: 'empty',
    fs: 'empty'
  }
};

module.exports = common;
