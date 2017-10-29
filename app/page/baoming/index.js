// page/baoming/index.js
Page({

  /**
   * 页面的初始数据
   */
  data: {
    items: [
      { name: '1', value: '周五晚' },
      { name: '2', value: '周六下午', checked: 'true' },
      { name: '3', value: '周六晚上' },
      { name: '4', value: '周天下午' },
      { name: '5', value: '周六晚上' },
      { name: '6', value: '其他' },
    ]
  },
  checkboxChange: function (e) {
    console.log('checkbox发生change事件，携带value值为：', e.detail.value)
  },
  formSubmit: function (e) {
    console.log(e.detail.value.checkbox.length, e.detail.value.checkbox[0], e.detail.value.checkbox[1], e.detail.value.checkbox.join(',')) 
    var app = getApp()
    console.log(app.globalData.userInfo) 


    //  将最新的用户信息更新到数据库中  {username: "1", gender: "男", nickname: "mike", weixin_id: "2", cellphone: "3"}
    var detaildata = app.globalData.userInfo

    console.log('detaildata=', detaildata)
    wx.request({
      method: "POST",
      url: 'https://www.qiaohequan.com/wx/baoming',
      data: {
        payload: {
          name: detaildata.username,
          nickname: detaildata.nickname,
          cellphone: detaildata.cellphone,
          gender: detaildata.gender,
          weixin_id: detaildata.weixin_id,
          level: detaildata.level,
          time: e.detail.value.checkbox.join(',')
        }

      },
      header: {
        "Content-Type": "application/json"
      },
      success: function (res) {
        var data = res.data;
        wx.showToast({
          title: '成功',
          icon: 'success',
          duration: 2000
        })
      }
    });



  },
  formReset: function () {
    console.log('form发生了reset事件')
  },
  baocun: function(){



  }
,

  // saoma: function(){
  //   wx.scanCode({
  //     success: (res) => {
  //       console.log(res)
  //     }
  //   })
  // }
// ,
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {

    var app = getApp()
    console.log(app.globalData.userInfo) // I am global data


    // wx.request({
    //   url: 'test.php', //仅为示例，并非真实的接口地址
    //   data: {
    //     x: '',
    //     y: ''
    //   },
    //   header: {
    //     "Content-Type": "application/json"
    //   },
    //   success: function (res) {
    //     console.log(res.data)
    //   }
    // })


  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
  
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})