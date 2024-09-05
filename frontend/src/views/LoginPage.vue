<script setup>

import router from "@/router/index"
async function loginUser() {
  
  const uname=document.getElementById('uname').value;
  const pw=document.getElementById('pw').value;
  const body={
    "username":uname,
    "password":pw
  };
  try{
    const res= await fetch("http://localhost:8080/api/UserLogin",{
      method:"POST",
      headers: {
        "Content-Type": "application/json"
      },
      redirect:"manual",
      body:JSON.stringify(body)
    })
    const result = await res.json();
    console.log(result);
    if (result.token!=null) {
      localStorage.setItem('token', result.token);
      router.push('/Home');
      
    }else{
      alert('username or password is incorrect');
    }
  }catch(err){
    console.log(err);
  }
  
}

</script>

<template>
  <main>
    <div id="main">
      <div class="card" id="login-card">
        <div class="card-body">
          <h3 style="text-align: center;">Login</h3>
          <form>

            <div class="mb-3">
              <label for="" class="form-label">User name</label>
              <input
                type="text"
                class="form-control"
                name="UserName"
                id="uname"
                aria-describedby="helpId"
                placeholder="username"
                required
              />
            </div>
            <div class="mb-3">
              <label for="" class="form-label">Password</label>
              <input
                type="password"
                class="form-control"
                name="password"
                id="pw"
                aria-describedby="helpId"
                placeholder="******"
                required
              />
            </div>
            <p>Don't have a account Register here</p>
            <RouterLink to="/Register">Click here</RouterLink><br>
            <div style="text-align: center;">

              <a href="#"  class="btn btn-primary"  @click="loginUser">Submit</a>
              <a href="/LibrarianLogin" class="btn btn-outline-primary" style="margin-left: 10px;">Librarian Login</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>
<style scoped>
main{
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