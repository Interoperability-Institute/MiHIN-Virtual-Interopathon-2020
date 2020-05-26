const merge = require("webpack-merge");
const path = require("path");
const webpack = require("webpack");
const common = require("./webpack.config.common.js");

module.exports = merge(common, {
  mode: "development",
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: "babel-loader"
      }
    ]
  },
  devServer: {
    contentBase: path.resolve(__dirname, "public"),
    port: 3005,
    https: false,
    host: "0.0.0.0",
    public: "0.0.0.0",
    hotOnly: true,
    historyApiFallback: {
      rewrites: [
        { from: /index/, to: "/index.html" },
        { from: /launch/, to: "/launch.html" },
        { from: /register/, to: "/register.html" }
      ]
    },
    proxy: [
      {
        context: ["/files", "/fhir", "/crd"],
        target: "https://xxxxx-xxxxx.interopland.com",
        changeOrigin: true,
        secure: true
      }
    ]
  },
  plugins: [new webpack.HotModuleReplacementPlugin()]
});
