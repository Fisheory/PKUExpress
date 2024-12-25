// components/bott-bar/bott-bar.js
Component({
  methods: {
    navigateToPage(event) {
      const page = event.currentTarget.dataset.page;
      const pages = getCurrentPages();
      const currentPage = pages[pages.length - 1];
      const pagePath = currentPage.route;
      const pageName = pagePath.split('/').pop();
      console.log("/?/")
      console.log(page);
      console.log("/?/")
      console.log(pageName);
      console.log("/?/")
      if (page != pageName){
        wx.redirectTo({
          url: `/pages/${page}/${page}`
        });
      }
    },
    navigateToAdd() {
      wx.redirectTo({
        url: '/pages/post/post'
      });
    }
  }
});
