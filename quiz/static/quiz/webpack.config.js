const path = require('path');

module.exports = {
    entry: './src/index.js',
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist')
    },
    module: {
        rules: [
            // { enforce: 'pre', test: /\.js$/, exclude: /node_modules/, loader: 'eslint-loader' }
            {test: /\.js$/, exclude: /node_modules/, loader: 'babel-loader'},
            {test: /\.json$/, loader: 'json-loader'},
            {test: /\.html/, loader: 'html-loader'},
            {test: /\.styl$/, loader: 'style-loader!css-loader!stylus-loader'},
            {test: /\.css$/, loader: 'style-loader!css-loader'},
            {test: /\.(gif|png|jpe?g)$/i, loader: 'file-loader?name=dist/images/[name].[ext]'},
            {
                test: /\.woff2?$/,
                loader: 'url-loader?name=dist/fonts/[name].[ext]&limit=10000&mimetype=application/font-woff'
            },
            {test: /\.(ttf|eot|svg)$/, loader: 'file-loader?name=dist/fonts/[name].[ext]'}
        ]
    }
};
