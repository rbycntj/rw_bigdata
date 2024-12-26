<template>
 <el-dialog title="登录" :visible.sync= "loginDialogFormVisible" :before-close="handleClose" :center="true" append-to-body width="23%" >
    <el-form label-position="left" label-width="80px" :rules="rules" ref="user" :model="user">
      <el-form-item label="账号" prop="account">
        <el-input v-model="username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="password" show-password maxlength="10" minlength="4"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button  @click="registerShow()" type="text"><div class="box1">注册</div></el-button>
        <el-button  @click="forgetShow()" type="text" ><div class="box1">忘记密码</div></el-button>
        <br/>
        <el-button @click="close()" type="primary" >取 消</el-button>
        <el-button @click="toLogin()" type="primary" >登录</el-button>
      </el-form-item>
        
    </el-form>
    
    
    
    <el-dialog title="注册" :visible.sync="registerDialogFormVisible" append-to-body :before-close="handleClose" centerDialogVisible = true width="35%" >
    <el-form label-position="left" label-width="80px" :rules="rules" ref="user" :model="user">
      <el-form-item label="姓名" prop="name">
        <el-input v-model="username"></el-input>
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="password" show-password  maxlength="10" minlength="4"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="confirmPassword" show-password  maxlength="10" minlength="4"></el-input>
      </el-form-item>
      <el-form-item label="性别" >
        <el-radio-group v-model="usersex">
          <el-radio label="男"></el-radio>
          <el-radio label="女"></el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="电话号码" prop="phone">
        <el-input v-model="userphone"></el-input>
      </el-form-item>
    </el-form>
      <el-button @click="loginShow()" type="primary"><div class="box2">取消</div></el-button>
      <el-button @click="toRegister()" type="primary"><div class="box2">注册</div></el-button>
    </el-dialog>


    <el-dialog title="找回密码" :visible.sync="forgetDialogFormVisible" append-to-body :before-close="handleClose" width="35%" >
    <el-form label-position="left" label-width="80px" :rules="rules" ref="user" :model="user">
      <el-form-item label="账号" prop="account">
        <el-input v-model="username"></el-input>
      </el-form-item>
      <el-form-item label="新密码" prop="password">
        <el-input v-model="password" show-password  maxlength="10" minlength="4"></el-input>
      </el-form-item>
      <el-form-item label="确认密码" prop="confirmPassword">
        <el-input v-model="confirmPassword" show-password maxlength="10" minlength="4"></el-input>
      </el-form-item>
      <el-form-item label="电话号码" prop="phone">
        <el-input v-model="userphone"></el-input>
      </el-form-item>
    </el-form>
    <el-button @click="loginShow()" type="primary"><div class="box2">取消</div></el-button>
    <el-button @click="toFind()" type="primary"><div class="box2">找回</div></el-button>
    </el-dialog>
  </el-dialog>
</template>

<script>
import {mapActions, mapMutations, mapState} from 'vuex'
export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: "Login",
  props: ["DialogFormVisible"],
  data() {
      return {
        user:{
          name:"",
          account:"",
          password:"",
          confirmPassword:"",
          type:"",
          sex:"",
          phone:"",
        },
        rules:{
          account:[
            { required: true, message: '请输入账号', trigger: 'blur' }
          ],
          name: [
            { required: true, message: '请输入姓名', trigger: 'blur' },
          ],
          password:[
            { required: true, message: '请输入密码', trigger: 'blur' },
            { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
          ],
          confirmPassword:[
            { required: true, message: '请输入确认密码', trigger: 'blur' },
            { min: 1, max: 10, message: '长度在 1 到 10 个字符', trigger: 'blur' }
          ],
          phone:[
            { required: true, message: '请输入电话号码', trigger: 'blur' }
          ]
        },
        loginDialogFormVisible:false,
        registerDialogFormVisible: false,
        forgetDialogFormVisible: false,
      };
    },
    watch:{
      DialogFormVisible:{
         handler(newValue){
           this.loginDialogFormVisible=newValue;
         }
      }
    },
    computed:{
        ...mapState('user',['loginStatus']),
    },
    methods:{
      ...mapActions('user',['loginUser']),
      ...mapActions('user',['registerUser']),
      ...mapActions('user',['fogetPasswordUser']),
      ...mapMutations('user',['logoutUser']),
      handleClose() {
        this.close();
      },
      clear(){
        this.user.name="";
        this.user.account="";
        this.user.password="";
        this.user.confirmPassword="";
        this.user.sex="男";
        this.user.phone="";
        this.loginDialogFormVisible = false;
        this.registerDialogFormVisible = false;
        this.forgetDialogFormVisible = false;
      },
      close(){
        this.clear();
        this.$emit("DialogVisible",false);
      },
      loginShow(){
        this.clear();
        this.loginDialogFormVisible = true;
      },
      registerShow(){
        this.clear();
        this.registerDialogFormVisible = true;
      },
      forgetShow(){
        this.clear();
        this.forgetDialogFormVisible = true;
      },
      toLogin(){
        if(this.user.account !=='' && this.user.password !==''){
          let person ={'account':this.user.account,'password':this.user.password};
          console.log("toLogin:person");console.log(person);
          this.loginUser(person)
          this.close();
        }else{
          this.$message({
          message: '用户名和密码不能为空',
          type: 'warning'
          });
        }
      },
      toRegister(){
        if(this.user.name =='' || this.user.password ==''){
          this.$message({
          message: '用户名和密码不能为空',
          type: 'warning'
          });
        }
        else if(this.user.password !== this.user.confirmPassword){
          this.$message({
          message: '两次输入密码不一致',
          type: 'warning'
          });
        }
        else{
          let person ={'username':this.user.name,'password':this.user.password,"sex":this.user.sex,"phone":this.user.phone};
          console.log(person);
          this.registerUser(person);
          this.close();
        }
      },
      toFind(){
        if(this.user.account =='' || this.user.password ==''){
          this.$message({
          message: '用户名和密码不能为空',
          type: 'warning'
          });
        }
        else if(this.user.password !== this.user.confirmPassword){
          this.$message({
          message: '两次输入密码不一致',
          type: 'warning'
          });
        }else{
          let person ={'account':this.user.account,'password':this.user.password,"phone":this.user.phone};
          console.log("toFindPWD:person");console.log(person);
          this.fogetPasswordUser(person);
          this.close();
        }
      }
    }

}
</script>

<style>
.box1 {
  display: inline-block;
  width: 100px;
  margin-bottom: 0px;
  text-align: left;
}

.box2 {
  display: inline-block;
  width: 200px;
  margin-bottom: 0px;
  text-align: center;
}

.el-button--primary {
  background: #3599F5 !important;
  border-color: #3599F5 !important;
}
</style>
