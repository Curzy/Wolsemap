var webpack = require('webpack');

module.exports = {
  context: __dirname,
  entry: {
    index: './index.js',
    wolsemap: './wolsemap.js'
  },
  output: {
    path: __dirname + '/../dist',
    filename: '[name].js'
  },
  module: {
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
    })
  ],
  externals: {
    'jquery': '$',
    'bson': 'bson'
  }
};
