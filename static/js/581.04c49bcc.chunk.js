"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[581],{1581:(e,s,t)=>{t.r(s),t.d(s,{default:()=>p});var a=t(5043),n=t(5173),r=t.n(n),i=t(7128),c=t(6213),l=t(2355),o=t(3946),d=t(3216),h=(t(9456),t(9426)),u=t(579);const m=(e,s,t)=>{const[n,r]=(0,a.useState)(!1),[m,x]=(0,a.useState)(null),{state:p,dispatch:j}=(0,a.useContext)(i.i),{accessToken:g,refreshToken:_,objectCount:b}=p,[v,f]=((0,d.Zp)(),(0,h.A)());return(0,u.jsxs)(o.qI,{className:"row g-3 needs-validation",noValidate:!0,validated:n,onSubmit:a=>{!1===a.currentTarget.checkValidity()&&(a.preventDefault(),a.stopPropagation()),r(!0);const n={division_slug:e,batch_name:m};a.preventDefault(),(async e=>{m||alert("Please Enter The Valid Batch Name");const a=c.A.create();let n={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},r=await f(v,a,"/manage/add_batch/","post",n,e,null);if(0==r.error){let e=r.response,a={...b};a.batches+=1,j({type:"GET_OBJECTS",payload:a}),s((s=>[...s,e.data.data])),t((e=>e+1)),(0,l.S)("success","Batch Added successfully...!")}else alert(r.errorMessage.message)})(n)},children:[(0,u.jsxs)(o.UF,{md:12,children:[(0,u.jsx)(o.A6,{htmlFor:"validationCustom01",children:"Batch Name"}),(0,u.jsx)(o.OG,{type:"text",id:"validationCustom01",onChange:e=>x(e.target.value),required:!0}),(0,u.jsx)(o.To,{valid:!0,children:"Looks good!"})]}),(0,u.jsx)(o.UF,{xs:12,children:(0,u.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},x=e=>{const[s,t]=(0,h.A)(),{state:n,dispatch:r}=(0,a.useContext)(i.i),{accessToken:x,refreshToken:p,semesters:j}=n,{division_slug:g,chageSteps:_,setBatchCout:b}=((0,d.Zp)(),e),[v,f]=(0,a.useState)([]);return(0,a.useEffect)((()=>{(async()=>{const e=c.A.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await(0,l.R)(e,"/manage/get_batches","get",s,null,{division_slug:g});if(0==t.error){let e=t.response;f(e.data.data)}else alert(t.errorMessage.message)})()}),[]),(0,u.jsxs)(u.Fragment,{children:[(0,u.jsx)(o.sK,{children:(0,u.jsx)(o.UF,{xs:12,children:(0,u.jsxs)(o.E$,{className:"mb-3",children:[(0,u.jsx)(o.V0,{children:(0,u.jsx)("strong",{children:"Batches"})}),(0,u.jsx)(o.W6,{children:m(g,f,b)})]})})}),(0,u.jsx)(o.sK,{children:(0,u.jsx)(o.UF,{xs:!0,children:(0,u.jsxs)(o.E$,{className:"mb-4",children:[(0,u.jsx)(o.V0,{children:(0,u.jsx)("strong",{children:"Batch History"})}),(0,u.jsx)(o.W6,{children:(0,u.jsxs)(o._v,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,u.jsx)(o.wV,{color:"light",children:(0,u.jsx)(o.YI,{className:"text-center",children:(0,u.jsx)(o.$s,{children:"Batch Name"})})}),(0,u.jsx)(o.jS,{children:v.map(((e,s)=>(0,u.jsx)(o.YI,{"v-for":"item in tableItems",children:(0,u.jsx)(o.cC,{children:(0,u.jsxs)("div",{className:"text-center",children:[e.division.division_name," | ",e.batch_name]})})},s)))})]})})]})})})]})};x.prototype={chageSteps:r().func.isRequired,semSlug:r().string};const p=x}}]);
//# sourceMappingURL=581.04c49bcc.chunk.js.map