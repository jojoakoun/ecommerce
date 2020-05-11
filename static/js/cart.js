// Let's query all the buttons by the class 'update-cart'
var updateBtns = document.getElementsByClassName('update-cart')

//we want to add an event handler in the loop 

for (i=0; i< updateBtns.length; i++) {
    updateBtns[i].addEventListener('click',function(){
        var productId = this.dataset.product //return the owner of the product.id
        var action = this.dataset.action // return the action to "add"
        console.log('productId:', productId, 'Action:', action)

        /*Let's console the user with two differents statements
        depending on whether the user is logged or not
        */
        console.log("USER:", user)
        if (user == "AnonymousUser") {
            addcookieItem(productId,action)
        }
        else {
           
            updateUserOrder(productId,action)
        }
       
        function addcookieItem(productId,action){
            console.log('User is not authenticated')

             //If the action is "add", we want to check if this item is already in the cart. 
             //If not, then we create it. If we already have that Item in our cart, 
             //we simply want to add to the quantity.
            if (action == "add") {
                if (cart[productId] == undefined){
                    cart[productId] = {'quantity':1}
                }
                else {
                    cart[productId]['quantity'] +=1
                }
            }
            //If the action is "remove", we want to either decrease the quantity, or, 
            //if the quantity is equal to or below zero, remove it from our cart altogether.
            if (action == "remove") {
                cart[productId]['quantity'] -=1
                if(cart[productId]['quantity'] <= 0){
                    console.log('Item should be deleted')
                    delete cart[productId];
                }
            }

            // we want to update the browser cookie
            console.log('CART:',cart)
            document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path/'
            location.reload()

        }
        
    })
    
}

/* We need to create a function that gets triggered if our user
    is logged and have that function send a POST request to our view
    (updateItem) */

function updateUserOrder(productId,action) {
    console.log('User is authenticated, sending some data')

    /*url variable to update_item and create 
    and use the fetch api to send a post request.*/
    var url = '/update_item/'
    fetch(url,{
        method: 'POST',
        headers: {
            'Content-Type' : 'application/json',
            'X-CSRFToken': csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action' : action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        //Now that we have the “csrftoken” variable set, we can pass it into our fetch() call.
        //This will alow us to see changes appear in our cart immediately once we render them.
        location.reload();
    })
}