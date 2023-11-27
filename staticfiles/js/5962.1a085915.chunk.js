"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[5962],{5962:(e,s,t)=>{t.r(s),t.d(s,{default:()=>j});var r=t(2791),a=(t(8682),t(2585)),n=t(5294),l=(t(2958),t(9434)),c=(t(9160),t(3645)),i=t(2937),o=t(7689),d=t(184);const h=function(e){let{visible:s,setVisible:t,SelectedTeacher:l}=e;const{state:h,dispatch:x}=(0,r.useContext)(a.y),{accessToken:j,refreshToken:u,currentBatch:m}=h,[b,g]=(0,r.useState)([]);(0,o.s0)();let p=b;const v=(e,s)=>{p.map((t=>{t==s&&(t.selected=e)}))};return(0,r.useEffect)((()=>{s&&(async()=>{const e=n.Z.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await(0,c.J)(e,"/manage/get_subjects_of_current_batch","get",s,null,{batch_slug:m.slug,teacher_id:l.id});if(0==t.error){let e=t.response;g(e.data.data)}else console.log(t.error)})()}),[s]),(0,d.jsx)(d.Fragment,{children:(0,d.jsxs)(i.N3,{className:"card w-100",style:{background:"#3c4b64"},placement:"end",visible:s,onHide:()=>t(!1),"data-coreui-backdrop":"static",children:[(0,d.jsxs)(i.Cu,{className:"card-header text-light",style:{background:"#303c54"},children:[(0,d.jsx)(i.XU,{children:l.profile.name}),(0,d.jsx)("button",{className:"btn btn-outline-light",onClick:()=>t(!1),children:(0,d.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-x-lg",viewBox:"0 0 16 16",children:(0,d.jsx)("path",{d:"M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"})})})]}),(0,d.jsx)(i.Cu,{className:"card-header text-light",style:{background:"#303c54"},children:(0,d.jsxs)(i.XU,{children:["Branch - ",l.branch.branch_name," | Batch - ",m.batch_name]})}),(0,d.jsx)(i.xF,{children:(0,d.jsx)(i.rb,{children:(0,d.jsx)(i.b7,{xs:!0,style:b.length>0?{}:{display:"flex",justifyContent:"center"},children:b.length>0?(0,d.jsxs)(i.xH,{className:"mb-4",children:[(0,d.jsx)(i.bn,{className:"text-center",children:(0,d.jsx)("strong",{children:"Subjects"})}),(0,d.jsxs)(i.sl,{children:[(0,d.jsxs)(i.Sx,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,d.jsx)(i.V,{color:"light",children:(0,d.jsxs)(i.T6,{children:[(0,d.jsx)(i.is,{children:"Name"}),(0,d.jsx)(i.is,{className:"text-center",children:"Code"}),(0,d.jsx)(i.is,{className:"text-center",children:"Action"})]})}),(0,d.jsx)(i.NR,{children:b.map(((e,s)=>(0,d.jsxs)(i.T6,{children:[(0,d.jsx)(i.NN,{children:(0,d.jsx)("div",{children:e.subject_name})}),(0,d.jsx)(i.NN,{className:"text-center",children:(0,d.jsx)("div",{children:e.code})}),(0,d.jsx)(i.NN,{className:"text-center",children:(0,d.jsx)("div",{children:e.selected?(0,d.jsx)(i.EC,{id:"flexCheckChecked-".concat(s),defaultChecked:!0,onChange:s=>v(s.target.checked,e)}):(0,d.jsx)(i.EC,{id:"flexCheckDefault-".concat(s),onChange:s=>v(s.target.checked,e)})})})]},s)))})]}),(0,d.jsx)("button",{className:"btn btn-outline-dark form-control mt-4",type:"submit",onClick:async()=>{g(p);let e=b.filter((e=>!0===e.selected)).map((e=>e.slug)),s={teacher_id:l.id,selected_subjects:e};await(async e=>{const s=n.Z.create();let r={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},a=await(0,c.J)(s,"/manage/add_subjects_to_teacher","post",r,e,null);0==a.error?(a.response,t(!1)):console.log(a.error);(0,c.w)("success","Subject Added successfully...!")})(s)},children:"Set Subject"})]})]}):(0,d.jsxs)(i.oo,{animation:!1,autohide:!1,visible:!0,children:[(0,d.jsxs)(i.xZ,{children:[(0,d.jsx)("svg",{className:"rounded me-2",width:"20",height:"20",xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMidYMid slice",focusable:"false",role:"img",children:(0,d.jsx)("rect",{width:"100%",height:"100%",fill:"#007aff"})}),(0,d.jsx)("div",{className:"fw-bold me-auto",children:"SMARTROLL ADMINISTRATION"})]}),(0,d.jsx)(i.S3,{children:"There are no subjects available...Please add some!"})]})})})})]})})},x=e=>{const[s,t]=(0,r.useState)(!1),{state:l,dispatch:h}=((0,o.s0)(),(0,r.useContext)(a.y)),{accessToken:x,refreshToken:j,currentBatch:u}=l,[m,b]=(0,r.useState)(""),[g,p]=(0,r.useState)(""),[v,f]=(0,r.useState)(""),[N,C]=(0,r.useState)("");console.log(u);return(0,d.jsxs)(i.lx,{className:"row g-3 needs-validation",noValidate:!0,validated:s,onSubmit:s=>{!1===s.currentTarget.checkValidity()&&(s.preventDefault(),s.stopPropagation()),s.preventDefault(),t(!0);(async s=>{const t=n.Z.create();let r={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},a=await(0,c.J)(t,"/manage/add_teacher","post",r,s,null);if(0==a.error){let s=a.response;e((e=>[...e,s.data.teacher]))}else console.log(a.error)})({name:m,email:g,ph_no:v,password:N}),(0,c.w)("success","Teacher Added successfully...!")},children:[(0,d.jsxs)(i.b7,{md:6,children:[(0,d.jsx)(i.L8,{htmlFor:"validationCustom01",children:"Teacher Name"}),(0,d.jsx)(i.jO,{type:"text",id:"validationCustom01",required:!0,onChange:e=>b(e.target.value)}),(0,d.jsx)(i.CO,{valid:!0,children:"Looks good!"})]}),(0,d.jsxs)(i.b7,{md:6,children:[(0,d.jsx)(i.L8,{htmlFor:"validationCustom01",children:"Teacher Moblie No"}),(0,d.jsx)(i.jO,{type:"tel",id:"validationCustom02",pattern:"[0-9]{10}",required:!0,onChange:e=>f(e.target.value)}),(0,d.jsx)(i.CO,{valid:!0,children:"Looks good!"})]}),(0,d.jsxs)(i.b7,{md:6,children:[(0,d.jsx)(i.L8,{htmlFor:"validationCustom01",children:"Teacher E-mail"}),(0,d.jsx)(i.jO,{type:"email",id:"validationCustom02",required:!0,onChange:e=>p(e.target.value)}),(0,d.jsx)(i.CO,{valid:!0,children:"Looks good!"})]}),(0,d.jsxs)(i.b7,{md:6,children:[(0,d.jsx)(i.L8,{htmlFor:"validationCustom02",children:"Teacher Password"}),(0,d.jsx)(i.jO,{type:"password",id:"validationCustom02",required:!0,onChange:e=>C(e.target.value)}),(0,d.jsx)(i.CO,{valid:!0,children:"Looks good!"})]}),(0,d.jsx)(i.b7,{xs:12,children:(0,d.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},j=()=>{const[e,s]=(0,r.useState)(!1),[t,j]=(0,r.useState)(!1),[u,m]=(0,r.useState)(null),[b,g]=((0,o.s0)(),(0,l.I0)(),(0,r.useState)([])),{state:p,dispatch:v}=(0,r.useContext)(a.y),{accessToken:f,refreshToken:N}=p;(0,r.useEffect)((()=>{(async()=>{const e=n.Z.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await(0,c.J)(e,"/manage/get_teachers","get",s);if(0==t.error){let e=t.response;g(e.data.teachers)}else console.log(t.error)})()}),[]);return(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(i.rb,{children:(0,d.jsx)(i.b7,{xs:12,children:(0,d.jsxs)(i.xH,{className:"mb-3",children:[(0,d.jsx)(i.bn,{children:(0,d.jsx)("strong",{children:"Teachers"})}),(0,d.jsx)(i.sl,{children:x(g)})]})})}),(0,d.jsx)(i.rb,{children:(0,d.jsx)(i.b7,{xs:!0,children:(0,d.jsxs)(i.xH,{className:"mb-4",children:[(0,d.jsx)(i.bn,{children:(0,d.jsx)("strong",{children:"Teacher History"})}),(0,d.jsx)(i.sl,{children:(0,d.jsxs)(i.Sx,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,d.jsx)(i.V,{color:"light",children:(0,d.jsxs)(i.T6,{children:[(0,d.jsx)(i.is,{children:"Name"}),(0,d.jsx)(i.is,{children:"E-mail"}),(0,d.jsx)(i.is,{children:"Mobile No"})]})}),(0,d.jsx)(i.NR,{children:b.map(((e,s)=>(0,d.jsxs)(i.T6,{"v-for":"item in tableItems",onClick:()=>{m(e),j(!0)},children:[(0,d.jsx)(i.NN,{children:(0,d.jsx)("div",{children:e.profile.name})}),(0,d.jsx)(i.NN,{children:(0,d.jsx)("div",{children:e.profile.email})}),(0,d.jsx)(i.NN,{children:(0,d.jsx)("div",{children:e.profile.ph_no})})]},s)))})]})})]})})}),u?(0,d.jsx)(h,{visible:t,setVisible:j,SelectedTeacher:u}):null]})}},8682:()=>{}}]);
//# sourceMappingURL=5962.1a085915.chunk.js.map