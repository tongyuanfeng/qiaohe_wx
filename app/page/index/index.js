
//获取应用实例
var app = getApp();
Page({
  data: {
    tb: "",
    banner3_title: "",
    banner3_img: "",
    banner3_desc_bg: "",

    imgUrls: [
      'https://raw.githubusercontent.com/tongyuanfeng/qiaohe_web/master/img/photo/010b12422c879bd030f53efc0feb17813ead0c70cb.jpg',
      '../../image/02.png',
      '../../image/03.png',
      '../../image/04.png',

    ],
    toutiaoUrls: [
      '文章标题1',
      '文章标题2',
      '文章标题3',
    ],
    indicatorDots: true,
    autoplay: true,
    interval: 2000,
    duration: 1000,
    menu: {
      imgUrls: [

        '../../image/推理.png',
        '../../image/狼人杀.png',
        // '../../image/book.png',
        '../../image/技能-1.png',
        '../../image/zaoqi.png',
        '../../image/战斗力.png'
      ],
      descs: [
        '剧本推理',
        '狼人杀',
        // '读书分享',
        '技能分享',
        '早起营地',
        '战斗力排行'
      ]
    }

  },
  //事件处理函数
  showloading: function () {
  },
  bindViewTap: function () {
  },
  onShow: function () {


    wx.getUserInfo({
      success: function (res) {
        var userInfo = res.userInfo
        var nickName = userInfo.nickName
        var avatarUrl = userInfo.avatarUrl
        var gender = userInfo.gender //性别 0：未知、1：男、2：女
        var province = userInfo.province
        var city = userInfo.city
        var country = userInfo.country
        app.globalData.userInfo = userInfo
      }
    })
    
 
    // app.globalData.userInfo.nickName
    wx.request({
      method: "POST",
      url: 'https://www.qiaohequan.com/wx/getuserinfo',
      data: {
        "payload": {
          "nickname": app.globalData.userInfo.nickName,
          "weixin_id": app.globalData.userInfo.weixin_id
        }

      },
      header: {
        "Content-Type": "application/json"
      },
      success: function (res) {
        var data = res.data;
        
        if (data.name==""){
          console.log(data) 
          console.log('aaa')
          wx.redirectTo({
            url: '../myqiaohe/index', /// todo  这里不生效
          })
        }


      }
    });


    //  wx.showNavigationBarLoading();
    wx.setNavigationBarTitle({
      title: '首页'
    })

 

  },
  onShareAppMessage: function () {
    return {
      title: '自定义分享标题',
      path: '/page/user?id=123',
      success: function (res) {
        // 分享成功
      },
      fail: function (res) {
        // 分享失败
      }
    }
  }
  ,
  ontouch_id: function () {

    wx.navigateTo({
      url: '../toutiao/index',
    })

  },

  ontouch_1: function () {

    wx.navigateTo({
      url: '../toutiao/index',
    })

  },

  ontouch_2: function () {

    wx.navigateTo({
      url: '../toutiao/index',
    })

  },

  ontouch_3: function () {

    wx.navigateTo({
      url: '../toutiao/index',
    })

  },

  onTouch_1: function () {
    console.log('onTouch_xxxxxxxxx')
    wx.navigateTo({
      url: '../juben/index',
    })
  },
  onTouch_2: function () {
    console.log('onTouch_2')
    wx.navigateTo({
      url: '../langren/index',
    })
  },
  onTouch_3: function () {
    console.log('touched')
    wx.navigateTo({
      url: '../jineng/index',
    })
  },
  onTouch_4: function () {
    console.log('touched')
    wx.navigateTo({
      url: '../zaoqi/index',
    })
  },

  onTouch_5: function () {
    console.log('onTouch_5')
    wx.navigateTo({
      url: '../zhandouli/index',
    })
  }
  
})