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
  mode: 'development',
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
        use: ['style-loader', 'css-loader'],
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
      'process.env.NODE_ENV': '"development"',
    }),
  ],
};