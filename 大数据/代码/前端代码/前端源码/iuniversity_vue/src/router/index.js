import VueRouter from "vue-router";

//引入组件
import UniversityList from "@/pages/UniversityList.vue";
import UniversityCount from "@/pages/UniversityCount.vue";
import UniversityMatch from "@/pages/UniversityMatch.vue";

//引入页面
const router = new VueRouter({
    routes: [{
            path: '/universityList',
            component: UniversityList
        },
        {
            path: '/universityCount',
            component: UniversityCount
        },
        {
            path: '/universityMatch',
            component: UniversityMatch
        },

        {
            path: "*",
            redirect: "/universityList"
        }
    ]
})

const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
    return originalPush.call(this, location).catch(err => err)
}


export default router