<template>
  <div class="topBar">
    <!--系统图标与名字-->
    <div style="display: flex;margin-left: 47px;" >
      <img src="../assets/icon/icon.png" class="iconStyle"/>
      <span class="fontStyle">iUniversity</span>
    </div>
    <!--用户信息按钮-->
    <el-popover
        placement="bottom-end"
        width="200"
        trigger="click">
      <div style="text-indent: 1em;font-size: 1em;font-weight: bold;color: rgba(33,33,33,0.7);">
        <div >
          <div class="loginText">个人中心</div>
          <div class="loginText">注销</div>
        </div>
      </div>
      <div class="user" slot="reference">
        <img src="../assets/icon/menu.png" style="width:18px;height:18px;margin-top: 12px;"/>
        <img src="../assets/icon/user.png" style="width:29px;height:29px;margin-top: 7px;"/>
      </div>
    </el-popover>

    <login :DialogFormVisible="DialogFormVisible" @DialogVisible="DialogVisible"></login>

  </div>
</template>

<script>
import login from "@/components/Login";
import {mapState} from "vuex";

export default {
  name: "TopBar",
  data() {
    return {
      DialogFormVisible: false,
    }
  },
  components: {
    login
  },
  computed: {
    ...mapState('user', ['loginStatus']),
  },
  methods: {
    showLogin() {
      if (this.loginStatus === false) {
        this.DialogFormVisible = true;
      } else {
        const h = this.$createElement;
        this.$msgbox({
          title: '消息',
          message: h('p', null, [h('span', null, '该操作将退出用户登录，是否继续？')]),
          showCancelButton: true,
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          beforeClose: (action, instance, done) => {
            if (action === 'confirm') {
              this.$store.state.user.commit('logoutUser');
              done();
            } else {
              done();
            }
          }
        }).then(() => {
          this.$message({
            type: 'success',
            message: '退出登录成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消退出登录'
          });
        });
      }
    },
    DialogVisible(DialogVisible) {
      this.DialogFormVisible = DialogVisible;
    },
    

  }
}
</script>

<style scoped lang="css">
.topBar {
  height: 50px;
  width: 100%;
  background-color: #ffffff;
  position: fixed;
  z-index: 5;
  padding: 15px 0px;
  display: flex;
  justify-content: space-between;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
}


/*图标样式*/
.iconStyle {
  width: auto;
  height: 50px;
  margin: 0;
  display: inline-block;
}

/*标题样式*/
.fontStyle {
  line-height: 50px;
  height: 50px;
  font-weight: bolder;
  font-size: 1.5em;
  text-indent: 0.5em;
  color: red;
  width: auto;
}

/*用户操作按钮*/
.user {
  margin-top: 4px;
  margin-right: 90px;
  height: 42px;
  width: 64px;
  border-radius: 23px;
  background-color: #ffffff;
  padding: 0 6px;
  display: flex;
  justify-content: space-around;
  align-content: center;
  border: 1px solid rgba(0, 0, 0, 0.2);
}

.user:hover {
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .04);
}

</style>

