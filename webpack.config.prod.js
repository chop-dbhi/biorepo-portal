const path = require('path');
const ROOT_PATH = path.resolve(__dirname);
const webpack = require('webpack');

module.exports = {
  entry: path.resolve(ROOT_PATH,
      'react_ui/index'),
  output: {
    path: path.resolve(ROOT_PATH, 'brp/static/js'),
    filename: 'bundle.js',
  },
  mode: 'production',
  module: {
    rules: [
      {
        test: /\.js$/,
        use: [{
          loader: 'babel-loader'
        }],
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: [
          { loader : 'style-loader'},
         {
          loader: 'css-loader',
          options: {
            modules: true,
            localIdentName: '[path][name]__[local]--[hash:base64:5]'
          }
      }
        ],
      },
    ],
  },
  externals: {
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
  plugins: [
    new webpack.DefinePlugin({
      'process.env.NODE_ENV': '"production"',
    }),
  ],
};