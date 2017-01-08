const webpack = require('webpack');
const merge = require('webpack-merge');
const Dashboard = require('webpack-dashboard');
const DashboardPlugin = require('webpack-dashboard/plugin');
const dashboard = new Dashboard();

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
      {test: /\.less$/, loader: 'style!css!less'},
      {test: /\.svg$/, loader: 'svg-loader'}
    ]
  },
  resolve: {
    root: __dirname,
    extensions: ['', '.js', '.jsx', 'css', 'les']
  },
  plugins: [
    new webpack.optimize.CommonsChunkPlugin({
      name: 'common',
      filename: 'commons.js',
      minChunks: 2
    }),
    new DashboardPlugin(dashboard.setData),
  ],
  node: {
    net: 'empty',
    tls: 'empty',
    fs: 'empty'
  }
};

module.exports = common;
