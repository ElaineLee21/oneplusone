        function get_beverages() {
            $("#post-box").empty()
            $.ajax({
                type: "GET",
                url: `/beverages`,
                data: {},
                success: function (response) {
                    if (response["result"] == "success") {
                        let posts = response["posts"]
                        console.log(response)
                        for (let i = 0; i < posts.length; i++) {
                            let post = posts[i]
                            //let likeCounts = post["count_heart"]
                            let conveni_store = post["conveni_store"]
                            let product_name = post["product_name"]
                            let product_price = post["product_price"]
                            let product_img = post["product_img"]
                            let likes = post["like"]

                            console.log(post)
                            //let class_heart = post['heart_by_me'] ? "fa-heart": "fa-heart-o"
                            let html_temp = `
                                            <div class="card" style="width: 18rem; height: 25rem;">
                                            <p>${conveni_store}</p>
                                                <img class="card-img-top" src="${product_img}" alt="Card image cap">
                                                <div class="card-body">
                                                   <p class="card-text">${product_name}</p>
                                                   <div class="price_like_box">
                                                   <p>${product_price}₩</p>
                                                   <button class="btn btn-outline" onclick="like_bev()"><i class="fa fa-heart-o" aria-hidden="true">${likes}</i></button>
                                                    </div>
                                                    
                                                     
                                                </div>
                                             </div>
                            `
                            $("#post-box").append(html_temp)
                        }
                    }
                }
            })
        }