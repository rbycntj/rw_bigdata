import axios from 'axios'
import { Message } from 'element-ui'

// create an axios instance
const service = axios.create({
    timeout: 5000 // request timeout
})

service.defaults.baseURL = "http://localhost:8080"

// request interceptor
service.interceptors.request.use(
    config => {
        return config
    },
    error => {
        // do something with request error
        console.log("##", error) // for debug
        return Promise.reject(error)
    }
)

// response interceptor
service.interceptors.response.use(
    response => {
        const res = response.data
            // if the custom code is not 20000, it is judged as an error.
        if (res.code !== 20111) {
            Message({
                message: res.message || 'Error',
                type: 'error',
                duration: 2000
            })
            return Promise.reject(new Error(res.message || 'Error'))
        } else {
            return res
        }
    },
    error => {
        console.log('err' + error) // for debug
        Message({
            message: error.message,
            type: 'error',
            duration: 2000
        })
        return Promise.reject(error)
    }
)

export default service