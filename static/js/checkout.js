if (user != 'AnonymousUser'){
  document.getElementById('user-info').innerHTML = '';
}

var deliveryOption = document.getElementsByName('pickup');
let buttonChecked = "delivery";


function isDeliveryClicked(){
  for(let i = 0; i < deliveryOption.length; i++){
    if(deliveryOption[i].checked){
      buttonChecked = deliveryOption[i].value;
      if(deliveryOption[i].value === "pickup"){
        let shippingAddressBlock = document.getElementById("shipping-form");
        shippingAddressBlock.classList.add("d-none");
      }else{
        let shippingAddressBlock = document.getElementById("shipping-form");
        shippingAddressBlock.classList.remove("d-none");
      }
    }
  }

var url = 'update_delivery_info/';

  fetch(url,{
    method: 'POST',
    headers:{
      'Content-Type' : 'application/json',
      'X-CSRFToken' : csrftoken,
    },
    body: JSON.stringify({
      'buttonChecked': buttonChecked,
      'orderId': orderId,
    })
  } )
  .then((response) => {
    return response.json();
  })
  .then((data) => {
    console.log('data: ', data);
  })
}


var form = document.getElementById('form')
csrftoken = form.getElementsByTagName("input")[0].value;

form.addEventListener('submit', (e)=>{
  e.preventDefault();
  document.getElementById('form-button').classList.add('d-none');
  document.getElementById('payment-info').classList.remove('d-none');
})

function submitFormData(){
  console.log('Payment buttons clicked');

  var userFormData = {
    'name':null,
    'email':null,
    'total': total,
  }

  var userShippingData = {
    'address':null,
    'city':null,
    'state':null,
    'zipcode':null,
  }

  console.log("delivery button: ", buttonChecked);

  if(buttonChecked == 'delivery'){
    userShippingData.address = form.address.value;
    userShippingData.city = form.city.value;
    userShippingData.state = form.state.value;
    userShippingData.zipcode = form.zipcode.value;
  }

  console.log(userShippingData)

  if(user == "AnonymousUser"){
    userFormData.name = form.name.value;
    userFormData.email = form.email.value;
  }

  var url="process_order/";

  fetch(url, {
    method:"POST",
    headers:{
      "Content-Type":"application/json",
      "X-CSRFToken": csrftoken,
    },
    body:
      JSON.stringify({
        'form': userFormData,
        'shipping': userShippingData,
      }),
  })
  .then((response)=>{
    response.json();
  })
  .then((data)=>{
    console.log("Success: ", data);
    alert("Transaction Complete");
    cart={};
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/";
    window.location.href= homePage;
  })
}
