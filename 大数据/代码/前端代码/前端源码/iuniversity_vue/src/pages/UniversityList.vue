<template>
  <div class="totalStyle">
    <div class="topBar">

      <!--中间搜索框-->
      <div class="searchBox" @click="drawerVisibleSearch=true">
        <div style="display: flex;height:22px;margin-top: 14px;">
          <div class="textStyle" style="border-right: 1px solid grey;">
            {{ searchObj.name === "" ? "任何地方" : searchObj.name }}
          </div>
          <div class="textStyle">{{ showDateRange === '' ? "任何学校" : showDateRange }}</div>
          <div v-show="false" style="text-align: center;width:88px;font-size: 14px;color: #717171;
                      font-weight: normal;line-height: 22px;">
          </div>
        </div>
        <div class="searchIcon" @click.stop="getHouses">
          <img src="../assets/icon/search.png" style="height:16px;width:16px;margin-top: 8px;">
        </div>
      </div>

      <el-popover
          placement="bottom"
          width="500"
          trigger="click">
        <div style="display: flex;">
          <v-distpicker province="北京市" city="北京市" area="大兴区" @area="onChangeArea"
                        @city="onChangeCity"></v-distpicker>
        </div>

        <el-button type="text" style="top: 23px;position: absolute;right: 0;" slot="reference">
          {{ searchObj.city }}、{{ area }}<i class="el-icon-arrow-down el-icon--right"></i>
        </el-button>
      </el-popover>
    </div>

    <div class="selectOptions">
      <div class="selectOption" v-for="item in searchOptions" :key="item.id"
           @click="chooseOption(item)" :style="nowChoose===item.id?{opacity:1}:{}">
        <img :src="require('../assets/icon/'+item.icon)" style="height:24px;width:24px;margin-left: 16px;"/>
        <span class="optionName">{{ item.name }}</span>
        <div v-show="nowChoose===item.id"
             style="height: 3px;background-color: black;margin-top: 13px;"></div>
      </div>
      <div class="screen" @click="dialogVisible=true">筛选条件</div>
    </div>



    <div class="content">
    <div class="table-container">
      <el-table :data="tableData" stripe row-key="id"
       :header-cell-style="{'text-align':'center',background:'#FFE4E1',color:'#000000'}"
       :cell-style="{'text-align':'center'}" default-expand-all 
       class="rounded-table" 
       @row-click="handleRowClick"
       :style="{ cursor: 'pointer' }"
       >
       <el-table-column sortable prop="school_name" label="学校"></el-table-column>
       <el-table-column sortable prop="school_level" label="学校层次"></el-table-column>
       <el-table-column prop="school_pos" sortable label="学校位置"></el-table-column>
       <el-table-column prop="school_type" sortable label="学校类型"></el-table-column>
       <el-table-column prop="sentiment_score" sortable label="评分"></el-table-column>
      </el-table>
    </div>

    <el-drawer
    title="学校详细信息"
    :visible.sync="drawerVisible"
    direction="rtl"
    size="30%"
    custom-class="custom-drawer"
  >
    <div v-if="selectedSchool" class="school-details">

      <el-row>
        <el-col :span="24">
          <el-card class="school-info-card">
            <el-card-body>
              <p><strong>学校名称:</strong> {{ selectedSchool.school_name }}</p>
              <p><strong>学校层次:</strong> {{ selectedSchool.school_level }}</p>
              <p><strong>QS排名:</strong> {{ selectedSchool.qs_rank }}</p>
              <p><strong>U.S. News排名:</strong> {{ selectedSchool.us_rank }}</p>
              <p><strong>软科排名:</strong> {{ selectedSchool.rk_rank }}</p>
              <p><strong>武书连排名:</strong> {{ selectedSchool.wsl_rank }}</p>
              <p><strong>艾瑞深校友会排名:</strong> {{ selectedSchool.xyh_rank }}</p>
              <p><strong>情感评分:</strong> {{ selectedSchool.sentiment_score }}</p>
            </el-card-body>
          </el-card>
          <el-card class="school-word">
            <el-card-body>
              <div ref="wordCloud" style="width: 100%; height: 400px;"></div>
            </el-card-body>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </el-drawer>
    
    </div>


    <div class="bottom">
      <span>© 2024 iUniversity, Chinese ·隐私 · 条款 · 网站</span>
      <span style="margin-left: 65%;color: black;font-weight: bold;">中文简体(CN)</span>
    </div>


    <!--搜索条件-->

    <el-drawer
        :visible.sync="Search"
        direction="ttb"
        size="100px"
        :with-header="false">
      <div style="width:100%;">
        <div class="options">

          <div class="inputInfo" :class="inputStatus===1?'inputActive': ''"
               @click="inputStatus=1" style="width:40%;">
            <div class="inputInfoText">
              <span>地点</span>
              <input v-model="searchObj.name" class="inputClass" placeholder="搜索目的地">
            </div>
          </div>

          <div class="inputInfo" style="width:40%;" :class="inputStatus===2?'inputActive': ''"
               @click="inputStatus=2">

            <el-popover
                placement="bottom"
                width="400"
                trigger="click">

              <div style="text-align: center;">
                <el-date-picker
                    v-model="dateRange"
                    value-format="yyyy-MM-dd"
                    type="daterange"
                    range-separator="至"
                    start-placeholder="开始日期"
                    end-placeholder="结束日期">
                </el-date-picker>
              </div>

              <div class="inputInfoText" slot="reference">
                <span>入住时间</span>
                <div style="display: flex;text-align: center;">
                  <input class="inputClass" disabled v-model="dateRange[0]" placeholder="添加日期">
                  至
                  <input class="inputClass" disabled v-model="dateRange[1]" placeholder="添加日期">
                </div>
              </div>
            </el-popover>
          </div>

          <div class="inputInfo" :class="inputStatus===3?'inputActive': ''"
               @click="inputStatus=3" style="display: flex;width:20%;">
            <el-popover v-if="false"
                        placement="bottom"
                        width="350"
                        trigger="click">
              <div
                  style="font-size: 1.2em;font-weight: bold;color: #212121;display: flex;line-height: 40px;height: 40px;">
                人数:
                <el-input-number style="width:250px;" class="inputClass" v-model="personNum" :min="0" :max="10"
                                 label="入住人数"></el-input-number>
              </div>
              <div class="inputInfoText" slot="reference" style="min-width: 166px;">
                <span>人员</span>
                <input class="inputClass" :value="personNumInfo" disabled placeholder="添加房客">

              </div>
            </el-popover>

            <div class="searchButton" @click="onClickSearch">
              <img src="../assets/icon/search.png"
                   style="height:20px;width:20px;margin-top: 14px;">搜索
            </div>
          </div>

        </div>
      </div>
    </el-drawer>

  </div>
</template>

<script>
import VDistpicker from 'v-distpicker';
import * as echarts from 'echarts';
import 'echarts-wordcloud';


export default {
  name: "UniversityList",
  components: {
    VDistpicker
  },
  data() {
    return {
      houseList: [],
      wordCloudData: [
    ],
      tableData:[],
      drawerVisible: false, 
      selectedSchool: null,
      drawerVisibleSearch: false, 
      priceRange: [0, 1800],
      dateRange: [],
      personNum: 0,
      sourceType: [],

      area: "大兴区",
      searchObj: {
        name: "",
        sourceType: null,
        bedNum: null,
        min: 0,
        max: 1800,
        city: "北京市",
        type: null,
        status: null
      },
      searchOptions: [
        {id: 0, icon: 'all.png', name: "全部"},
        {id: 1, icon: 'jiudian.png', name: "统计" },
        {id: 2, icon: 'minsu.png', name: "匹配"},

      ],
      nowChoose: 0,
      inputStatus: 1,
      dialogVisible: false,
    }
  },
  mounted() {
    this.getUniversities();
    this.initWordCloud();
    console.log(this.$el);
  },
  computed: {
    personNumInfo() {
      return this.personNum === 0 ? "" : this.personNum + '人'
    },
    showDateRange() {
      let string = ''
      if (this.dateRange.length !== 0) {
        string += this.dateRange[0].split('-')[1] + '月' + this.dateRange[0].split('-')[2] + '日'
        string += "至"
        string += this.dateRange[1].split('-')[1] + '月' + this.dateRange[1].split('-')[2] + '日'
      }
      return string
    }
  },
  methods: {
    handleRowClick(row) {
      this.selectedSchool = row; 
      this.wordCloudData = this.selectedSchool.keywords;
      this.drawerVisible = true;  
      
      this.$nextTick(() => {
      this.initWordCloud();  
  });

      console.log(this.selectedSchool);
    },


    getUniversities() {
      const params = {
    "topN": "10" 
  };
      this.$axios.post('http://82.157.131.132:8000/bigdata/get_all_schools', params, {
    headers: {
      'Content-Type': 'application/json' 
    }
  })
  .then((res) => {
    if (res.status === 200) {
      this.tableData = res.data.data;
      console.log(this.tableData);
    } else {
      console.error('请求失败，状态码：', res.status);
    }
  })
  .catch((error) => {
    console.error('发生错误：', error);
  });
    },

    chooseOption(item) {
      this.nowChoose = item.id
      if (item.id ===1 ) {
        this.$router.push('/universityCount'); }
      else if (item.id ===2) {
        this.$router.push('/universityMatch'); 
      }
      this.searchObj.type = item.name === "全部" ? null : item.name
      this.getHouses()
    },
    

    initWordCloud() {
      const chartDom = this.$refs.wordCloud;
      const myChart = echarts.init(chartDom);

      const option = {
        series: [{
          type: 'wordCloud',
          gridSize: 1,
          size: ['50%', '50%'],
          textStyle: {
              fontFamily: '微软雅黑',
              color: function () {
                  return 'rgb(' + [
                    Math.round(Math.random() * 255),
                    Math.round(Math.random() * 255),
                    Math.round(Math.random() * 255)
                  ].join(',') + ')';
                }
            },
          data: this.wordCloudData
        }]
      };

      myChart.setOption(option);
      //window.addEventListener('resize', () => myChart.resize());
    }
  },

}
</script>

<style scoped lang="css">

.table-container {
  overflow: hidden; /* 确保子元素不超出边界 */
  border-radius: 16px; /* 设置圆角半径 */
}

.rounded-table {
  border-collapse: separate; /* 避免单元格之间的合并 */
  border-spacing: 0; /* 移除单元格之间的间距 */
}

.rounded-table .el-table__header,
.rounded-table .el-table__body {
  border-radius: 16px; /* 设置表头和表体的圆角 */
}

.rounded-table .el-table__header th:first-child {
  border-top-left-radius: 16px; /* 左上角圆角 */
}

.rounded-table .el-table__header th:last-child {
  border-top-right-radius: 16px; /* 右上角圆角 */
}

.rounded-table .el-table__body tr:last-child td:first-child {
  border-bottom-left-radius: 16px; /* 左下角圆角 */
}

.rounded-table .el-table__body tr:last-child td:last-child {
  border-bottom-right-radius: 16px; /* 右下角圆角 */
}

.totalStyle {
  width: 100%;
  /*background-color: aquamarine;*/
}


.topBar {
  height: 50px;
  background-color: rgba(255, 255, 255, 0.99);
  position: fixed;
  top: 0;
  z-index: 10;
  padding: 15px 0;
  display: flex;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
  justify-content: space-between;
  width: 65%;
  left: 17.5%;
}

/*搜索框*/
.searchBox {
  width: 320px;
  height: 47px;
  margin: auto;
  border-radius: 28px;
  display: flex;
  justify-content: space-around;
  border: 1px solid rgba(0, 0, 0, 0.08);
  box-shadow: 0 2px 4px rgba(0, 0, 0, .12), 0 0 6px rgba(0, 0, 0, .02);
}

.searchBox:hover {
  box-shadow: 0 4px 4px rgba(0, 0, 0, .10), 0 0 6px rgba(0, 0, 0, 0.08);
}

.searchIcon {
  background-color: #f61616;
  height: 32px;
  width: 32px;
  border-radius: 16px;
  text-align: center;
  margin-top: 8px;
  margin-left: -12px;
}

.textStyle {
  text-align: center;
  width: 120px;
  font-size: 14px;
  font-weight: bold;
  line-height: 22px;
}

.selectOptions {
  height: 64px;
  background-color: #ffffff;
  position: sticky;
  top: 81px;
  left: 0;
  z-index: 6;
  padding: 16px 80px 0;
  border-bottom: 1px solid rgba(0, 0, 0, 0.2);
  display: flex;
}

/*单个搜素条件*/
.selectOption {
  display: flex;
  flex-direction: column;
  width: 56px;
  height: 64px;
  margin-right: 60px;
  text-align: center;
  opacity: 0.6;
}

.selectOption:hover {
  opacity: 1;
}

.screen {
  height: 40px;
  width: 100px;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  line-height: 40px;
  text-align: center;
  font-size: 0.9em;
  font-weight: bold;
}

.optionName {
  margin-top: 8px;
  line-height: 16px;
  height: 16px;
  color: #000000;
  font-size: 12px;
  font-weight: bold;
}

.content {
  margin-top: 80px;
  /*background-color: #1a8c1c;*/
  min-height: calc(100vh - 210px);
  padding-left: 60px;
  padding-right: 20px;
  padding-top: 20px;
}

.bottom {
  height: 18px;
  /*background-color: burlywood;*/
  position: fixed;
  bottom: 0;
  width: 100%;
  border-top: 1px solid rgba(0, 0, 0, 0.2);
  background-color: #ffffff;
  z-index: 10;
  padding: 10px 80px;
  line-height: 18px;
  color: #222222;
  font-size: 14px;
}

.dialogTitle {
  font-size: 22px;
  color: #222222;
  font-weight: bold;
}

.options {
  max-width: 50%;
  background-color: rgba(221, 221, 221, 1);
  height: 64px;
  margin: 18px auto;
  border-radius: 32px;
  display: flex;
  flex-direction: row;
  border: 1px solid rgba(0, 0, 0, 0.2);
}

.searchButton {
  display: flex;
  justify-content: space-around;
  height: 48px;
  width: 70%;
  border-radius: 24px;
  background-color: red;
  margin: 8px 0 0 15%;
  line-height: 48px;
  color: white;
  font-size: 1.1em;
  font-weight: bold;
}

.inputInfo {
  border-radius: 32px;
}

.inputActive {
  border-radius: 32px;
  background-color: #ffffff;
}

.inputInfoText {
  text-align: center;
  height: 36px;
  margin-top: 14px;
  border-right: 1px solid rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  font-size: 0.9em;
  font-weight: bold;
  color: #212121;
}

.inputClass {
  border: 0px;
  outline: none;
  width: 80%;
  margin-left: 10%;
  background-color: rgba(221, 221, 221, 0);
  text-align: center;
  font-weight: bold;
  color: #212121;
  font-size: 1.1em;
}



.school-details {
  color: #333; /* 字体颜色 */
  font-family: 'Arial', sans-serif; /* 字体样式 */
}

.school-info-card {
  background-color: #f9f9f9; /* 卡片背景颜色 */
  border-radius: 8px; /* 卡片圆角 */
  padding: 20px; /* 卡片内边距 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 卡片阴影 */
  margin-top:-10px;
}

.school-word {
  background-color: #ffffff; /* 卡片背景颜色 */
  border-radius: 8px; /* 卡片圆角 */
  padding: 5px; /* 卡片内边距 */
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); /* 卡片阴影 */
  margin-top:20px;
}

</style>


