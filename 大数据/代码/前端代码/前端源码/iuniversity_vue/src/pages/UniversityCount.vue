<template>
  <div class="totalStyle">
    <div class="topBar">

      <!--中间搜索框-->
      <div class="searchBox" @click="drawerVisible=true">
        <div style="display: flex;height:22px;margin-top: 14px;">
          <div class="textStyleSearch" style="border-right: 1px solid grey;">
            {{ searchObj.name === "" ? "任何地方" : searchObj.name }}
          </div>
          <div class="textStyleSearch">{{ showDateRange === '' ? "任何学校" : showDateRange }}</div>
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
      <!--筛选条件-->
      <div class="screen" @click="dialogVisible=true">筛选条件</div>
    </div>


   <div class="content">
    <div class="table-container">
      <div class="chart-wrapper">
      <div id="wordCloud"  class="chart"></div>
      <div id="barChart"  class="chart"></div>
    </div>
    </div>
   </div>

    <div class="bottom">
      <span>© 2024 iUniversity, Chinese ·隐私 · 条款 · 网站</span>
      <span style="margin-left: 65%;color: black;font-weight: bold;">中文简体(CN)</span>
    </div>


    <!--搜索条件-->
    <el-drawer
        :visible.sync="drawerVisible"
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
              </div>

              <div class="inputInfoText" slot="reference">
                <span>学校名称</span>
              
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
  name: "UniversityCount",
  components: {
    VDistpicker
  },
  data() {
    return {
      houseList: [],
      priceRange: [0, 1800],
      dateRange: [],
      personNum: 0,
      sourceType: [],
      wordCloudData: [
      ],
      barChartData: [
      ],


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
      nowChoose: 1,//当前选中类型
      inputStatus: 1,//1表示输入地址，2表示输入日期，3表示输入人数

      //弹窗界面出现控制
      dialogVisible: false,
      drawerVisible: false,
    }
  },
  mounted() {
    this.load_graph_word();  
    this.load_graph_province();  
  },
  computed: {
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
    chooseOption(item) {
      this.nowChoose = item.id
      if (item.id === 0) {
        this.$router.push('/universityList'); 
      } 
        else if (item.id ===2) {
          this.$router.push('/universityMatch'); 
      }
      this.searchObj.type = item.name === "全部" ? null : item.name
      this.getHouses()
    },

  load_graph_word() {
    const params = {
      "topN": "10" 
  };
    this.$axios.post('http://82.157.131.132:8000/bigdata/get_global_keywords', params, {
     headers: {
      'Content-Type': 'application/json'
     }
  })
  .then((res) => {
    if (res.status === 200) {
      this.wordCloudData = res.data.data;
      this.initWordCloud();
      console.log(this.wordCloudData);
    } else {
      console.error('请求失败，状态码：', res.status);
    }
  })
},

load_graph_province() {
    const params = {
    "topN": "10" 
  };
    this.$axios.post('http://82.157.131.132:8000/bigdata/get_province_count', params, {
     headers: {
      'Content-Type': 'application/json' 
     }
  })
  .then((res) => {
    if (res.status === 200) {
      this.barChartData = res.data.data; 
      this.initBarChart();
      console.log(this.barChartData);
    } else {
      console.error('请求失败，状态码：', res.status);
    }
  })
},
  
    initWordCloud() {
      const chartDom = document.getElementById('wordCloud');
      const myChart1 = echarts.init(chartDom);
    
    const wordCloudDataWithColors = this.wordCloudData.map(item => ({
      name: item.name,
      value: item.value,
    }));
 
    const option = {
      title: {
        text: '学生最关注的',
        left: 'center', 
        top: '3%', 
        textStyle: {
            fontSize: 24,
            fontFamily: '微软雅黑', 
            color: '#333'
        }
    },
      series: [{
        type: 'wordCloud',
        gridSize: 6,
        sizeRange: [20, 80],
        rotationRange: [-90, 90],
        shape: 'circle',
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
        data: wordCloudDataWithColors 
      }]
    };

    myChart1.setOption(option, true);
    window.addEventListener("resize", myChart1.resize); 
  },


    initBarChart() {
      const chartDom1 = document.getElementById('barChart');
      const myChart = echarts.init(chartDom1);
      
      const option = {
        title: {
        text: '不同省份的高校分布',
        left: 'center', 
        top: '3%', 
        textStyle: {
            fontSize: 24, 
            fontFamily: '微软雅黑',
            color: '#333'
        }
    },
        xAxis: {
          type: 'category',
          data: this.barChartData.map(item => item.region) 
        },
        yAxis: {
          type: 'value'
        },
        series: [{
          data: this.barChartData.map(item => item.count),
          type: 'bar',
          itemStyle: {
            color: '#87CEFA',
            borderColor: '#4682B4',
            borderWidth: 2
          }
        }]
      };

      myChart.setOption(option);
    }


  },

}
</script>

<style scoped lang="css">
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

.chart-wrapper {
  display: flex; /* 使图表并排 */
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

.table-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

#wordCloud, #barChart {
  border: 1px solid #ccc; /* 添加边框以便观察 */
  margin-bottom: 20px; /* 图表间距 */
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

.textStyleSearch {
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
  padding-left: 20px;
  padding-top: 40px;
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


.chart {
  width: 600px; /* 图表宽度 */
  height: 400px; /* 图表高度 */
  margin: 0 10px; /* 图表间距 */
  border-radius: 10px; /* 圆角 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}


</style>
