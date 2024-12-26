<template>
<div>
  <div :style="{'height':'100px'}"></div>
  <el-row :gutter="5">
  <el-col :span="4"><div class="grid-content"></div></el-col>
  <el-col :span="10"><div class="grid-content">
    <el-descriptions class="margin-top" title="个人信息" :column="1"  border>
    <template slot="extra">
       <el-button type="primary" icon="el-icon-edit" circle v-show="!InputVisible" @click="beginEdit()"></el-button>
       <el-button type="success" icon="el-icon-check" circle v-show="InputVisible" @click="endEdit()"></el-button>
    </template>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-user"></i>
        姓名
      </template>
      <div v-show="!InputVisible">{{user.username}}</div>
      <el-input v-model="personName" v-show="InputVisible"></el-input>
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-user"></i>
        昵称
      </template>
      <div v-show="!InputVisible">{{user.nickname}}</div>
      <el-input v-model="personNickname" v-show="InputVisible"></el-input>
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-s-check"></i>
        账号
      </template>
      {{user.account}}
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-location-outline"></i>
        密码
      </template>
      <div v-show="!InputVisible">{{user.password}}</div>
      <el-input v-model="personPassword" v-show="InputVisible"></el-input>
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-picture"></i>
        头像
      </template>
      <div v-show="!InputVisible">{{user.avatar}}</div>
      <el-input v-model="personAvatar" v-show="InputVisible"></el-input>
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-user-solid"></i>
        性别
      </template>
      <el-radio-group v-model="personSex" :disabled="!InputVisible">
        <el-radio label="男"></el-radio>
        <el-radio label="女"></el-radio>
      </el-radio-group>
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-mobile-phone"></i>
        电话号码
      </template>
      <div v-show="!InputVisible">{{user.phone}}</div>
      <el-input v-model="personPhone" v-show="InputVisible"></el-input>
    </el-descriptions-item>
    <el-descriptions-item>
      <template slot="label">
        <i class="el-icon-mobile-phone"></i>
        权限
      </template>
      {{getUserType()}}
    </el-descriptions-item>
  </el-descriptions>
  </div></el-col>
  <el-col :span="6"><div class="grid-content">
  <div class="edge">

  <el-row><el-col :span="24">
    <div class="grid-content">
    <img src="../assets/personViewImg/personViewImg0.png" class="pictrue"/>
    <p class="title">为什么我的信息未显示在此处？</p>
    <p class="page">我们隐藏了一些账号详细信息，以便保护您的身份。</p>
    </div>
  </el-col></el-row>
  <div class="line"></div>
  <el-row><el-col :span="24">
    <div class="grid-content">
    <img src="../assets/personViewImg/personViewImg1.png" class="pictrue"/>
    <p class="title">哪些详细信息可以编辑？</p>
    <p class="page">您可以编辑联系方式和个人信息。如果您此前在身份认证时使用了此信息，那么您需要在下次预订或者继续出租房源/开展体验时再次通过认证。</p>
    </div>
  </el-col></el-row>
  <el-row><el-col :span="24">
    <div class="grid-content">
    <img src="../assets/personViewImg/personViewImg2.png" class="pictrue"/>
    <p class="title">有哪些信息与其他人共享？</p>
    <p class="page">只有在订单确认后，ihome才会向房东和房客提供联系信息。</p>
    </div>
  </el-col></el-row>
  </div>
  </div></el-col>
  <el-col :span="4"><div class="grid-content"></div></el-col>
  </el-row>
  <div :style="{height:'60px','background-color':'#e4edf4'}"></div>
</div>
</template>

<script>
  import { mapState,mapGetters,mapActions} from "vuex"

export default {
  name: 'userInformationView',
  mounted() {
    this.personName=this.user.username;
    this.personNickname=this.user.nickname;
    this.personPassword=this.user.password;
    this.personPhone=this.user.phone;
    this.personAvatar=this.user.avatar;
    this.personSex=this.getUserSex();
    this.$bus.$emit("changeTopStyle", {
      'background-color': '#E8EbE4',
      'color': '#000'
    })
  },
  computed:{
    ...mapState('user',['user']),
    
  },
  data() {
      return {
        personName:"",
        personNickname:"",
        personPassword:"",
        personPhone:"",
        personAvatar:"",
        personSex:"",
        InputVisible:false
      };
  },
  methods:{
    ...mapGetters('user',['getUserName','getUserSex','getUserType']),
    ...mapActions('user',['EditPersonInformation']),
    beginEdit(){
      this.InputVisible=true;
    },
    endEdit(){
      this.InputVisible=false;
      console.log(this.personName==this.user.username&&this.personNickname==this.user.nickname&&
      this.personPassword==this.user.password&&this.personPhone==this.user.phone&&
      this.personAvatar==this.user.avatar&&this.personSex==this.getUserSex());
      if(this.personName==this.user.username&&this.personNickname==this.user.nickname&&
      this.personPassword==this.user.password&&this.personPhone==this.user.phone&&
      this.personAvatar==this.user.avatar&&this.personSex==this.getUserSex()){
        ;
      }else if(this.personName==""||this.personNickname==""||this.personPassword==""||
      this.personPhone==""||this.personAvatar==""||this.personSex==""){
        this.$message({
          message: '不能把信息修改为空',
          type: 'warning'
          });
      }
      else{
        const h = this.$createElement;
        this.$msgbox({
          title: '消息',
          message: h('p', null, [h('span', null, '是否保存修改？')]),
          showCancelButton: true,
          confirmButtonText: '是',
          cancelButtonText: '否',
          beforeClose: (action, instance, done) => {
            console.log('this.user.id');console.log(this.user.id);
            if (action === 'confirm') {
              let editPerson = {"id":this.user.id,"name":this.personName,"nickname":this.personNickname,
              "sex": this.personSex,"avatar":this.personAvatar,
              "password": this.personPassword,"phone":this.personPhone}
              if(editPerson.sex=="男"){
                editPerson.sex=0;
              }else{
                editPerson.sex=1;
              }
              this.EditPersonInformation(editPerson);
              done();
            } else {
              done();
            }
          }
        }).then(() => {
          this.$message({
            type: 'success',
            message: '修改成功!'
          });
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消修改'
          });          
        });
            }

      }
    
  }
}
</script>

<style>
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
  }
  .content{
    width:250px;
    height:250px;
  }
  .picture{
    width:150px;
    height:100px;
  }
  .title{
    margin-top: 16px !important;
    margin-left:30px !important;
    margin-right:30px !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    box-sizing: border-box;
    font-family: Circular, -apple-system, BlinkMacSystemFont, Roboto, Helvetica Neue, sans-serif;
    line-height: 1.43;
    color: #222;
  }
  .page{
    text-align:left;
    margin-top: 16px !important;
    margin-left:30px !important;
    margin-right:30px !important;
    font-size: 16px !important;
    color: #717171 !important;
    box-sizing: border-box;
    font-family: Circular, -apple-system, BlinkMacSystemFont, Roboto, Helvetica Neue, sans-serif;
    line-height: 1.43;
  }
  .edge{
    overflow:hidden;
    border:1px solid #DDDDDD !important;
    border-radius: 12px !important;
  }
  .line{
    border-bottom: 1px solid #DDDDDD !important;
    margin-left:32px;
    margin-right:32px;
  }
</style>