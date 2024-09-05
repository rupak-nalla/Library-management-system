
<script setup>
  import router from "@/router/index"
  async function validate(){
    const password=document.getElementById('password').value;
    const repatPw=document.getElementById('RepeatPw').value;
    if(password.length<8){
      alert('password must contain 8 or more then 8 charecters')
      return false
    }
    const capitalLetterRegex = /[A-Z]/;
    if( !capitalLetterRegex.test(password)){
      alert("must contain atleast one uppercase alphabet")
      return false
    }
    const NumRegex = /[0-9]/;
    if(!NumRegex.test(password)){
      alert("must contain atleast one number");
      return false
    }
    if(repatPw!==password){
      alert('Repeat password and password are not same');
      return false;
    }
    return true;
  }
async function HandleRegister() {
  try{
    if (await validate()==false){
      return '';
    }else{
      const uname=document.getElementById('username').value;
      const pw=document.getElementById('password').value;
      const email=document.getElementById('email').value;
      const body={
        "username":uname,
        "password":pw,
        "Email":email
      };
    
      const res= await fetch("http://localhost:8080/api/Register",{
        method:"POST",
        headers: {
          "Content-Type": "application/json"
        },
        redirect:"manual",
        body:JSON.stringify(body)
      })
      const contentType = res.headers.get("Content-Type");
      let result;

      if (contentType && contentType.indexOf("application/json") !== -1) {
        result = await res.json();
      } else {
        result = await res.text();
      }
      if (res.status==200) {
        console.log(result);
        alert('registration successful');
        router.push('/');
      }
      else if(res.status==409){
        alert(result);
      }
      else if(res.status==404){
        console.log(result);
      }
    }
    
    
    
  }catch(err){
    console.log(err)
  }
  
}
</script>

<template>
  <div id="main" style="height: fit-content;">
      <div class="card" id="login-card" style="margin: 10px;">
        <div class="card-body">
          <h3 style="text-align: center;">Registration</h3>
          <form>

            <div class="mb-3">
              <label for="" class="form-label">User name</label>
              <input
                type="text"
                class="form-control"
                name="UserName"
                id="username"
                aria-describedby="helpId"
                placeholder="username"
                required
              />
            </div>
            <div class="mb-3">
              <label for="" class="form-label">Email</label>
              <input
                type="email"
                class="form-control"
                name="email"
                id="email"
                aria-describedby="helpId"
                placeholder="email@example.com"
                required
              />
            </div>
            <div class="mb-3">
              <label for="" class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                name="password"
                id="password"
                aria-describedby="helpId"
                placeholder="******"
                required
              />
              
            </div>
            <div class="mb-3">
              <label for="" class="form-label">repeat Password</label>
              <input
                type="password"
                class="form-control"
                name="RepeatPassword"
                id="RepeatPw"
                aria-describedby="helpId"
                placeholder="******"
                required
              />
              
            </div>
            <p>Already have a account? Login here</p>
            <RouterLink to="/">Click here</RouterLink><br>
            <div>
              <h4>Password must contain following:</h4>
              <ul>
                <li>must contain 8 or more then 8 charecters</li>
                <li>must contain atleast one number</li>
                <li>must contain atleast one uppercase alphabet</li>
              </ul>
            </div>
            <div style="text-align: center;">

              <a @click="HandleRegister" class="btn btn-primary" >Submit</a>
            </div>
          </form>
        </div>
      </div>
    </div>
</template>

<style scoped>
#main{
  background-color: #e4e4e4;
  width: 100%;
  height: 500px;
  display: flex;
  justify-content: center;
  align-items: center;
}
#login-card{
  width: 300px;
  min-height: 300px;
  height: fit-content;
}
</style>
