// utils/http.js
import axios from 'axios'

const http = axios.create({
    baseURL: 'http://localhost:8000/api',
    timeout: 10000
})


export default http