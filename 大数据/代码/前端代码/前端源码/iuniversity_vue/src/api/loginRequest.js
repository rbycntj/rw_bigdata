import request from '@/utils/request'

export function login(person) {
  console.log("login:person");console.log(person);
  return request({
    url: '/person/login',
    method: 'post',
    params:person,
  })
}
export function register(person) {
  if(person.sex=="男"){
    person.sex=0;
  }else{
    person.sex=1;
  }
  console.log("register:person");console.log(person);
  return request({
    url: '/person/register',
    method: 'post',
    params:person,
  })
}
export function forgetPassword(person) {
  console.log("forget:person");console.log(person);
  return request({
    url: '/person/forgetPassword',
    method: 'post',
    params:person,
  })
}
export function editPerson(person){
  console.log("edit:person");console.log(person);
  return request({
    url: '/person/editPerson',
    method: 'post',
    params:person,
  })
}
