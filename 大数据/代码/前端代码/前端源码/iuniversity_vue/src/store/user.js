import {login,register,forgetPassword,editPerson} from "@/api/loginRequest";
import Vue from 'vue';
export default {
    // 开启命名空间
    namespaced: true,
    // state 数据
    state: () => ({
        loginStatus: false,
        user: {
            id: -1,
            account: "",
            username: "",
            password: "",
            sex: 0,
            type: 0,
            phone: "",
            avatar: "",
            nickname: ""
        }
    }),
    getters: {
        getUserName(state) {
            return state.loginStatus ? state.user.username : "请登录";
        },
        getUserSex(state) {
            return state.user.sex ? state.user.sex : "None";
        },
        getUserType(state) {
            return state.user.type ? state.user.type : "Error";
        }
    },
    mutations: {
        loginStatusSetFalse(state) {
            state.loginStatus = false;
        },
        clearUser(state) {
            state.loginStatus = false;
            state.user = {account: "", username: "", password: "", sex: "", type: "", phone: "", avatar: ""};
        },
        logoutUser(state) {
            state.loginStatus = false;
            state.user = {account: "", username: "", password: "", sex: "", type: "", phone: "", avatar: ""};
            delete localStorage.token;
        },
        LOGINUSER(state, response) {
            var user = {
                id: response.data.person.id,
                account: response.data.person.account,
                username: response.data.person.name,
                password: response.data.person.password,
                sex: response.data.person.sex,
                type: response.data.person.type,
                phone: response.data.person.phone,
                avatar: response.data.person.avatar,
                nickname: response.data.person.nickname
            }
            user.sex = (user.sex== 0 ? "男" : "女");
            user.type = (user.type== 0 ? "管理员":(user.type == 1 ? "房东":"租客"))
            state.loginStatus = true;
            state.user = user;
        }
    },
    actions: {
        loginUser(context, obj) {
            login(obj).then(
                response => {
                    console.log("登录完成");
                    console.log(response)
                    if (response.data !== null) {
                        context.commit('LOGINUSER', response)
                        localStorage.token = response.data.token;
                        console.log("token");
                        console.log(localStorage.token);
                    } else {
                        context.commit('clearUser');
                        Vue.prototype.$message({
                            type:"error",   
                            message:"登录失败"  
                            });
                    }
                }
            )
        },
        registerUser(context, obj) {
            register(obj).then(
                response => {
                    console.log("注册完成");
                    console.log(response)
                    if (response.data !== null) {
                        context.commit('LOGINUSER', response)
                        localStorage.token = response.data.token;
                        console.log("token");
                        console.log(localStorage.token);
                    } else {
                        context.commit('clearUser');
                        Vue.prototype.$message({
                            type:"error",   
                            message:"注册失败"  
                            });
                    }
                }
            )
        },
        fogetPasswordUser(context, obj) {
            forgetPassword(obj).then(
                response => {
                    console.log("修改密码完成");
                    console.log(response)
                    if (response.data !== null) {
                        context.commit('LOGINUSER', response)
                        localStorage.token = response.data.token;
                        console.log("token");
                        console.log(localStorage.token);
                    } else {
                        context.commit('clearUser');
                        Vue.prototype.$message({
                            type:"error",   
                            message:"修改密码失败"  
                            });
                    }
                }
            )
        },
        EditPersonInformation(context, obj) {
            console.log("obj");
            console.log(obj);
            editPerson(obj).then(
                response => {
                    console.log("个人信息修改完成");
                    console.log(response)
                    if (response.data !== null) {
                        context.commit('LOGINUSER', response);
                        console.log("token");
                        console.log(localStorage.token);
                    } else {
                        context.commit('clearUser');
                        Vue.prototype.$message({
                            type:"error",   
                            message:"个人信息修改失败"  
                            });
                    }
                }
            )
        },
    },
}
