// page/myqiaohe/index.js

 

Page({

  /**
   * 页面的初始数据
   */
  data: {
    user_touxiang:"",
    username:"",
    nickname:"",
    cellphone:"",
    gender:0,
    weixin_id:"",
    level:"F"
  },

  formSubmit: function (e) {
    console.log('form发生了submit事件，携带数据为：', e.detail.value)
  //  将最新的用户信息更新到数据库中  {username: "1", gender: "男", nickname: "mike", weixin_id: "2", cellphone: "3"}
    var detaildata = e.detail.value
    wx.request({
      method:"POST",
      url: 'https://www.qiaohequan.com/wx/update_userinfo', 
      data: {
        payload:{
          name: detaildata.username,
          nickname: detaildata.nickname,
          cellphone: detaildata.cellphone,
          gender: detaildata.gender,
          weixin_id: detaildata.weixin_id,
          level: detaildata.level
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
  }
  ,
  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    // other.js
    var app = getApp()
    console.log(app.globalData.userInfo) // I am global data
    var page = this
    page.setData({ nickname: app.globalData.userInfo.nickName})
    page.setData({ gender: app.globalData.userInfo.gender })
    page.setData({ user_touxiang: app.globalData.userInfo.avatarUrl })

    // page.setData({ name: app.globalData.userInfo.name })
    // page.setData({ cellphone: app.globalData.userInfo.cellphone })
    // page.setData({ weixin_id: app.globalData.userInfo.weixin_id })
    // page.setData({ level: app.globalData.userInfo.level })

    
    //  根据nickName从数据库中查询其他信息 -- 填充
    wx.request({     
      method: "POST",
      url: 'https://www.qiaohequan.com/wx/getuserinfo', 
      data: {
        "payload":{
          "nickname": app.globalData.userInfo.nickName,
          "weixin_id": page.data.weixin_id
        }
    
      },
      header: {
        "Content-Type": "application/json"
      },
      success: function (res) {
        var data = res.data;
         
        page.setData({ username: data.name})
        page.setData({ cellphone: data.cellphone })
        page.setData({ weixin_id: data.weixin_id })
        page.setData({ level: data.level })

        
      }
    });

   



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