module.exports = {
	entry: "./jsx/index.jsx",
	output: {
		path: __dirname + "/dist/js",
		filename: "bundle.js"
	},
	module: {
		loaders: [
			{
				test: /\.jsx?$/,
				exclude: /node_modules/,
				//include: [__dirname + "/jsx"],
				loader: "babel-loader",
				query: {"presets": ["es2015", "react"]}
			}
		]
	},
	resolve: {
		extensions: ["", ".js", ".jsx"],
		root: [
			"./jsx"
		]
	}
};
