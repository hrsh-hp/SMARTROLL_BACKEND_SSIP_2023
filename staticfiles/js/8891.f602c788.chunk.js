"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[8891],{2958:(e,r,t)=>{t.d(r,{I:()=>s,t:()=>a});const a="",s=""},8891:(e,r,t)=>{t.r(r),t.d(r,{default:()=>f});var a=t(2791),s=t(5294),l=t(7689),o=t(1087),n=t(2585),c=t(2958);t(8114);const d=async(e,r)=>{s.Z.post("".concat(c.t,"/auth/api/token/refresh/"),{refresh:e},{headers:{"ngrok-skip-browser-warning":!0}}).then((e=>{localStorage.setItem("accessToken",e.data.access),localStorage.setItem("refreshToken",e.data.refresh),r(!0)})).catch((e=>{}))};t(2673);var u=t(1134),i=t(2937),p=t(184);function f(){const e=(0,l.s0)(),{register:r,handleSubmit:t}=(0,u.cI)(),{state:f,dispatch:m}=(0,a.useContext)(n.y),{refreshToken:b,set404:g}=f;return(0,a.useEffect)((()=>{g&&(e("/404"),m({type:"SET_404",payload:!1}))}),[g]),(0,p.jsx)("div",{className:"h-screen bg-center bg-no-repeat sm:p-20 p-6",style:{background:"black"},children:(0,p.jsx)("section",{className:"w-full h-full flex justify-center items-center rounded-md bg-clip-padding backdrop-filter backdrop-blur-sm bg-opacity-20 border border-gray-100",style:{backgroundImage:"url(/static/images/background2.jpg)"},children:(0,p.jsxs)("div",{className:"text-white sm:w-full",children:[(0,p.jsxs)("form",{className:"max-w-sm mx-auto",onSubmit:t((r=>{if(r.enrollment!=parseInt(r.enrollment))return alert("please enter the valid enrollment numner ");s.Z.post("".concat(c.t,"/auth/api/register/"),{enrollment:r.enrollment,email:r.email,password:r.password},{header:{"Content-Type":"application/json","ngrok-skip-browser-warning":!0}}).then((r=>{r.data.data.status&&e("/login")})).catch((e=>{"ERR_NETWORK"===e.code?m({type:"SET_404",payload:!0}):401===e.response.status?d(b):alert("something went worng")}))})),autoComplete:"off",children:[(0,p.jsxs)("div",{className:"relative border-b-2\tborder-slate-500 z-0 w-full mb-5 group",children:[(0,p.jsx)("input",{type:"text",name:"floating_enrollment",id:"floating_enrollment",className:"block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer",placeholder:" ",required:!0,...r("enrollment")}),(0,p.jsx)("label",{htmlFor:"floating_email",className:"peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6",children:"Entrollment No."})]}),(0,p.jsxs)("div",{className:"relative border-b-2\tborder-slate-500 z-0 w-full mb-5 group",children:[(0,p.jsx)("input",{type:"email",name:"floating_email",id:"floating_email",className:"block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer",placeholder:" ",required:!0,...r("email")}),(0,p.jsx)("label",{htmlFor:"floating_email",className:"peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6",children:"Email address"})]}),(0,p.jsxs)("div",{className:"relative z-0 border-b-2\tborder-slate-500 w-full mb-5 group",children:[(0,p.jsx)("input",{type:"password",name:"floating_password",id:"floating_password",className:"block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer",placeholder:"",required:!0,...r("password")}),(0,p.jsx)("label",{htmlFor:"floating_email",className:"peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-75 top-3 -z-10 origin-[0] peer-focus:start-0 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-6",children:"Password"})]}),(0,p.jsx)("button",{type:"submit",className:"w-100 focus:ring-4  font-medium rounded-lg text-sm w-full sm:w-auto px-5 py-2.5 text-center  text-slate-300",style:{border:"1px solid #ffa31a"},children:"Register"})]}),(0,p.jsx)(i.rb,{className:"justify-center mt-4",children:(0,p.jsx)(i.b7,{className:"w-full text-center",children:(0,p.jsxs)("div",{children:[" Or ",(0,p.jsx)(o.rU,{to:"/login",className:"ml-2",style:{color:"rgb(255, 163, 26)"},children:"Login"})]})})})]})})})}},2673:()=>{},8114:()=>{}}]);
//# sourceMappingURL=8891.f602c788.chunk.js.map