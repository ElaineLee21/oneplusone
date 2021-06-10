function toggle_like(post_id) {
    const type = "like";
    let $button_like = $(`#${post_id} button[aria-label='heart']`)
    let $i_like = $button_like.find("i")
    console.log($i_like.hasClass("fa-heart"))
    if ($i_like.hasClass("fa-heart")) {
        $.ajax({
            type: "POST",
            url: "/likes",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "unlike"
            },
            success: function (response) {
                console.log("unlike")
                $i_like.addClass("fa-heart-o").removeClass("fa-heart")
                $button_like.find("span.like-num").text(response["count"])
            }
        })
    } else {
        $.ajax({
            type: "POST",
            url: "/likes",
            data: {
                post_id_give: post_id,
                type_give: type,
                action_give: "like"
            },
            success: function (response) {
                console.log("like")
                $i_like.addClass("fa-heart").removeClass("fa-heart-o")
                $button_like.find("span.like-num").text(response["count"])
            }
        })

    }
    window.location.reload()
}

function get_beverages() {
    $("#post-box").empty()
    $.ajax({
        type: "GET",
        url: `/beverages`,
        data: {},
        success: function (response) {
            if (response["result"] == "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]

                    let eachId = post["_id"]
                    let likeCounts = post["count_like"]
                    let conveni_store = post["conveni_store"]
                    let product_name = post["product_name"]
                    let product_price = post["product_price"]
                    let product_img = post["product_img"]

                    let class_heart = post['like_by_me'] ? "fa-heart" : "fa-heart-o"

                    let html_temp = `
                                        <div id= ${eachId} class="card" style="width: 18rem; height: 25rem;">
                                            <p class="card_cvs" id="cvs_name">${conveni_store}</p>
                                            <img class="card-img-top" src="${product_img}" alt="Card image cap">
                                            <div class="card-body">
                                               <p class="product_name">${product_name}</p>
                                                    <span class="price_like">
                                                       ${product_price}₩
                                                       <button class="btn btn-outline" aria-label="heart" onclick='toggle_like("${eachId}")' >
                                                           <i class="fa ${class_heart}" aria-hidden="true">
                                                           <span class="like-num">${likeCounts}</span></i>
                                                       </button>
                                                    </span>
                                         </div>
                                         </div> 
                                    `
                    $("#post-box").append(html_temp)
                }
            }
        }
    })
}

// ES6 함수작성법 이것과 위에 펑션은 똑같은 기능
const onClickLogOut = () => {
    console.log("click")
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃 되었습니다.')
    window.location.href = "/login"
}

const handleButtonClick = (store) => {
    $("#post-box").empty()
    let storeName = store;
    $.ajax({
        type: "GET",
        url: `/beverages`,
        data: {},
        success: function (response) {
            if (response["result"] === "success") {
                let posts = response["posts"]
                for (let i = 0; i < posts.length; i++) {
                    let post = posts[i]
                    let each_store = post["conveni_store"]
                    console.log(each_store)


                    if (storeName === each_store) {
                        let eachId = post["_id"]
                        let likeCounts = post["count_like"]
                        let product_name = post["product_name"]
                        let product_price = post["product_price"]
                        let product_img = post["product_img"]
                        let conveni_store = storeName
                        let class_heart = post['like_by_me'] ? "fa-heart" : "fa-heart-o"

                        let html_temp = `
                                            <div id= ${eachId} class="card" style="width: 18rem; height: 25rem;">
                                                <p class="card_cvs" id="cvs_name">${conveni_store}</p>
                                                <img class="card-img-top" src="${product_img}" alt="Card image cap">
                                                <div class="card-body">
                                                   <p class="product_name">${product_name}</p>
                                                        <span class="price_like">
                                                           ${product_price}₩
                                                           <button class="btn btn-outline" aria-label="heart" onclick='toggle_like("${eachId}")' >
                                                               <i class="fa ${class_heart}" aria-hidden="true">
                                                               <span class="like-num">${likeCounts}</span></i>
                                                           </button>
                                                        </span>
                                             </div>
                                             </div>
                                        `
                        $("#post-box").append(html_temp)
                    }
                }

            }
        }
    })
}