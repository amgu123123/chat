import { io } from "socket.io-client";
const socket = io("http://localhost:8000", {
    transports: ["websocket"],
    path: "/socket.io",
    withCredentials: true,
    // auth:{
    //     token:'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJncW0iLCJleHAiOjE3NDU5MjU5NzR9.87eumvdCN_r4YY55P3kiER0ikOiy0A7GcUxY6R-rd-0'
    // }
});

socket.on("connect", () => console.log("Connected!"));
socket.on("connect_error", (err) => console.error(err));