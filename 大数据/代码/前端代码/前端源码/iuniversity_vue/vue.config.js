const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
        transpileDependencies: true,
        devServer: {
            proxy: {
                '/api': {
                    target: 'http://localhost:8080',
                    pathRewrite: { '^/api': '' },
                    ws: true,
                    changeOrigin: true,
                },
                '/get_all_schools': {
                    target: 'http://127.0.0.1:8000',
                    changeOrigin: true,
                },
                '/get_global_keywords': {
                    target: 'http://127.0.0.1:8000',
                    changeOrigin: true,
                },
                '/get_province_count': {
                    target: 'http://127.0.0.1:8000',
                    changeOrigin: true,
                },
                '/predict': {
                    target: 'http://127.0.0.1:8000',
                    changeOrigin: true,
                },
            }
        }
    },

)