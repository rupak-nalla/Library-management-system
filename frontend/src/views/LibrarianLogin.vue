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
    const res= await fetch("http://localhost:8080/api/Librarian",{
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
      alert("Logged in");
      localStorage.setItem('token', result.token);
      router.push('/LibrarianDashBoard');
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
    <div id="main" style="display: flex;justify-content: center;align-items: center;">
      <div class="card" id="login-card">
        <div class="card-body">
          <h3 style="text-align: center;">Librarian Login</h3>
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
            <p>Not the Librarian <a href="/">Click here</a></p>
            <div style="text-align: center;">

              <a type="submit" @click="loginUser()" class="btn btn-primary" >Submit</a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </main>

</template>
<style scoped>
#main{
  background-color: #eceaea;
  height: 100%;
  min-height: 500px;
}
#side-bar{
     background-color: #e2e2e2;
     
     width: 250px;
}
#login-card{
  width: 300px;
  min-height: 300px;
  height: fit-content;
}
</style>