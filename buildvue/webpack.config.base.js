'use strict'

// const HtmlWebpackPlugin = require('html-webpack-plugin')
// const CopyWebpackPlugin = require('copy-webpack-plugin')
const { VueLoaderPlugin } = require('vue-loader')

const utils = require('./utils')

module.exports = {
  context: utils.resolve('assets/js'),
  entry: {
    blocksley: './blocksley.js'
  },
  output: {
    filename: 'js/[name].js',
    path: utils.resolve('blogsley/static'),
    publicPath: '/static/'
  },
  resolve: {
    extensions: ['.js', '.vue', '.json'],
    alias: {
      app: utils.resolve('./node_modules/@blocksley/applet/'),
      src: utils.resolve('./node_modules/@blocksley/applet/src'),
      assets: utils.resolve('./node_modules/@blocksley/applet/src/assets'),
      boot: utils.resolve('./node_modules/@blocksley/applet/src/boot'),
      layouts: utils.resolve('./node_modules/@blocksley/applet/src/layouts'),
      pages: utils.resolve('./node_modules/@blocksley/applet/src/pages'),
    }
  },

  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [
          /node_modules\/(?!@blocksley\/applet\/)/
          // /node_modules/
        ],
        use: {
          loader: 'babel-loader',
        }
      },
      {
        test: /\.vue$/,
        use: 'vue-loader'
      }, 
      {
        test: /\.(png|jpe?g|gif|svg)(\?.*)?$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10000,
            name: utils.assetsPath('img/[name].[hash:7].[ext]')
          }
        }
      },
      {
        test: /\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10000,
            name: utils.assetsPath('media/[name].[hash:7].[ext]')
          }
        }
      },
      {
        test: /\.(woff2?|eot|ttf|otf)(\?.*)?$/,
        use: {
          loader: 'url-loader',
          options: {
            limit: 10000,
            name: utils.assetsPath('fonts/[name].[hash:7].[ext]')
          }
        }
      }
    ]
  },

  plugins: [
    /*
    new HtmlWebpackPlugin({
      filename: 'index.html',
      template: 'index.html',
      inject: true
    }),
    */
    new VueLoaderPlugin(),
    /*
    new CopyWebpackPlugin([{
      from: utils.resolve('src/statics'),
      to: utils.resolve('dist/statics'),
      toType: 'dir'
    }])
    */
  ]
}
