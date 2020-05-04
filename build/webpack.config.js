const path = require('path');
const webpack = require('webpack')
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const utils = require('./utils')

const devMode = process.env.NODE_ENV !== 'production';

const STATIC_PATH = 'share/blogsley-flask-site/static/'
// const PUBLIC_PATH = '/static/'
const PUBLIC_PATH = '/'

module.exports = {
  watch: true,
  mode : devMode ? 'development' : 'production',
  // devtool: 'source-map',
  context: utils.resolve('assets/js'),
  entry: {
    main: './main.js',
    events: './events.js', 
    calendar: './calendar.js',
    dashboard: './dashboard.js',
    chart: './chart.js',
    postedit: './postedit.js',
    // blocksley: './blocksley.js'
  },
  output: {
    filename: 'js/[name].js',
    path: utils.resolve(STATIC_PATH),
    publicPath: PUBLIC_PATH
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
      chunkFilename: "[id].css"
    }),
    new webpack.ProvidePlugin({
      $: 'jquery',
      jQuery: 'jquery'
    }),
    new webpack.ProvidePlugin({
      Chart: 'chart.js'
    })
  ],
  module: {
    rules: [
      {
        test: /\.s?[ac]ss$/,
        use: [
            { 
              loader: MiniCssExtractPlugin.loader,
              options: {
                outputPath: utils.resolve(`${STATIC_PATH}css`),
                publicPath: utils.resolve(`${PUBLIC_PATH}css`)
              }
            },
            { loader: 'css-loader', options: { sourceMap: true } },
            {
              loader: 'resolve-url-loader'
            },
            { loader: 'sass-loader', options: { sourceMap: true } }
        ],
      },
      {
        test: /\.(png|gif|jpe|jpg|woff|woff2|eot|ttf|svg)(\?.*$|$)/,
        use: [
          {
            loader: 'url-loader',
            options: {
              limit: 64,
              outputPath: 'fonts',
              publicPath: '/fonts'
            }
          }
        ]
      }
    ]
  }
};