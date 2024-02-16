"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[962],{5962:(e,s,t)=>{t.r(s),t.d(s,{default:()=>b});var a=t(2791),n=(t(8682),t(2585)),r=t(5294),l=(t(2958),t(9434)),i=(t(9160),t(3645)),c=t(2937),d=t(7689),o=t(184);const h=function(e){let{visible:s,setVisible:t,SelectedTeacher:l}=e;const{state:h,dispatch:x}=(0,a.useContext)(n.y),{accessToken:j,refreshToken:m,currentBatch:u}=h,[b,g]=(0,a.useState)([]);(0,d.s0)();let p=b;const f=(e,s)=>{p.map((t=>{t==s&&(t.selected=e)}))};return(0,a.useEffect)((()=>{s&&(async()=>{const e=r.Z.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await(0,i.J)(e,"/manage/get_subjects_of_current_batch","get",s,null,{batch_slug:u.slug,teacher_id:l.id});if(0==t.error){let e=t.response;g(e.data.data)}})()}),[s]),(0,o.jsx)(o.Fragment,{children:(0,o.jsxs)(c.N3,{className:"card w-100",style:{background:"#3c4b64"},placement:"end",visible:s,onHide:()=>t(!1),"data-coreui-backdrop":"static",children:[(0,o.jsxs)(c.Cu,{className:"card-header text-light",style:{background:"#303c54"},children:[(0,o.jsx)(c.XU,{children:l.profile.name}),(0,o.jsx)("button",{className:"btn btn-outline-light",onClick:()=>t(!1),children:(0,o.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-x-lg",viewBox:"0 0 16 16",children:(0,o.jsx)("path",{d:"M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"})})})]}),(0,o.jsx)(c.Cu,{className:"card-header text-light",style:{background:"#303c54"},children:(0,o.jsxs)(c.XU,{children:["Branch - ",l.branch.branch_name," | Batch - ",u.batch_name]})}),(0,o.jsx)(c.xF,{children:(0,o.jsx)(c.rb,{children:(0,o.jsx)(c.b7,{xs:!0,style:b.length>0?{}:{display:"flex",justifyContent:"center"},children:b.length>0?(0,o.jsxs)(c.xH,{className:"mb-4",children:[(0,o.jsx)(c.bn,{className:"text-center",children:(0,o.jsx)("strong",{children:"Subjects"})}),(0,o.jsxs)(c.sl,{children:[(0,o.jsxs)(c.Sx,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,o.jsx)(c.V,{color:"light",children:(0,o.jsxs)(c.T6,{children:[(0,o.jsx)(c.is,{children:"Name"}),(0,o.jsx)(c.is,{className:"text-center",children:"Code"}),(0,o.jsx)(c.is,{className:"text-center",children:"Action"})]})}),(0,o.jsx)(c.NR,{children:b.map(((e,s)=>(0,o.jsxs)(c.T6,{children:[(0,o.jsx)(c.NN,{children:(0,o.jsx)("div",{children:e.subject_name})}),(0,o.jsx)(c.NN,{className:"text-center",children:(0,o.jsx)("div",{children:e.code})}),(0,o.jsx)(c.NN,{className:"text-center",children:(0,o.jsx)("div",{children:e.selected?(0,o.jsx)(c.EC,{id:"flexCheckChecked-".concat(s),defaultChecked:!0,onChange:s=>f(s.target.checked,e)}):(0,o.jsx)(c.EC,{id:"flexCheckDefault-".concat(s),onChange:s=>f(s.target.checked,e)})})})]},s)))})]}),(0,o.jsx)("button",{className:"btn btn-outline-dark form-control mt-4",type:"submit",onClick:async()=>{g(p);let e=b.filter((e=>!0===e.selected)).map((e=>e.slug)),s={teacher_id:l.id,selected_subjects:e};await(async e=>{const s=r.Z.create();let a={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},n=await(0,i.J)(s,"/manage/add_subjects_to_teacher","post",a,e,null);0==n.error&&(n.response,t(!1));(0,i.w)("success","Subject Added successfully...!")})(s)},children:"Set Subject"})]})]}):(0,o.jsxs)(c.oo,{animation:!1,autohide:!1,visible:!0,children:[(0,o.jsxs)(c.xZ,{children:[(0,o.jsx)("svg",{className:"rounded me-2",width:"20",height:"20",xmlns:"http://www.w3.org/2000/svg",preserveAspectRatio:"xMidYMid slice",focusable:"false",role:"img",children:(0,o.jsx)("rect",{width:"100%",height:"100%",fill:"#007aff"})}),(0,o.jsx)("div",{className:"fw-bold me-auto",children:"SMARTROLL ADMINISTRATION"})]}),(0,o.jsx)(c.S3,{children:"There are no subjects available...Please add some!"})]})})})})]})})};var x=t(9792),j=t(2062),m=t.n(j);const u=e=>{const[s,t]=(0,a.useState)(!1),{state:l,dispatch:h}=((0,d.s0)(),(0,a.useContext)(n.y)),{accessToken:j,refreshToken:u,currentBatch:b}=l,[g,p]=(0,x.Z)();return(0,o.jsxs)(c.lx,{className:"row g-3 needs-validation",noValidate:!0,validated:s,onSubmit:s=>{s.preventDefault();s.currentTarget;const a=s.target.tname.value,n=s.target.tmobile.value,l=s.target.temail.value;if(t(!0),a&&n&&l){(async s=>{const t=r.Z.create();let a=await p(g,t,"/manage/add_teacher/","post",{"Content-Type":"application/json","ngrok-skip-browser-warning":!0},s,null);if(0==a.error){let s=a.response;e((e=>[...e,s.data.data]))}})({name:a,email:l,ph_no:n}),(0,i.w)("success","Teacher Added successfully...!")}else m()({title:"Input Field Empty",icon:"error",button:"OK"})},children:[(0,o.jsxs)(c.b7,{md:6,children:[(0,o.jsx)(c.L8,{htmlFor:"validationCustom01",children:"Teacher Name"}),(0,o.jsx)(c.jO,{type:"text",id:"validationCustom01",name:"tname",required:!0}),(0,o.jsx)(c.CO,{valid:!0,children:"Looks good!"})]}),(0,o.jsxs)(c.b7,{md:6,children:[(0,o.jsx)(c.L8,{htmlFor:"validationCustom01",children:"Teacher Moblie No"}),(0,o.jsx)(c.jO,{type:"tel",id:"validationCustom02",name:"tmobile",pattern:"[0-9]{10}",required:!0}),(0,o.jsx)(c.CO,{valid:!0,children:"Looks good!"})]}),(0,o.jsxs)(c.b7,{md:12,children:[(0,o.jsx)(c.L8,{htmlFor:"validationCustom01",children:"Teacher E-mail"}),(0,o.jsx)(c.jO,{type:"email",id:"validationCustom02",name:"temail",required:!0}),(0,o.jsx)(c.CO,{valid:!0,children:"Looks good!"})]}),(0,o.jsx)(c.b7,{xs:12,children:(0,o.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},b=()=>{const[e,s]=(0,x.Z)(),[t,i]=(0,a.useState)(!1),[j,m]=(0,a.useState)(!1),[b,g]=(0,a.useState)(null),[p,f]=((0,d.s0)(),(0,l.I0)(),(0,a.useState)([])),{state:N,dispatch:v}=(0,a.useContext)(n.y),{accessToken:k,refreshToken:C}=N;(0,a.useEffect)((()=>{(async()=>{const t=r.Z.create();let a=await s(e,t,"/manage/get_teacher","get",{"Content-Type":"application/json","ngrok-skip-browser-warning":!0});if(0==a.error){let e=a.response;f(e.data.data)}else console.log(a.errorMessage.message)})()}),[]);return(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(c.rb,{children:(0,o.jsx)(c.b7,{xs:12,children:(0,o.jsxs)(c.xH,{className:"mb-3",children:[(0,o.jsx)(c.bn,{children:(0,o.jsx)("strong",{children:"Teachers"})}),(0,o.jsx)(c.sl,{children:u(f)})]})})}),(0,o.jsx)(c.rb,{children:(0,o.jsx)(c.b7,{xs:!0,children:(0,o.jsxs)(c.xH,{className:"mb-4",children:[(0,o.jsx)(c.bn,{children:(0,o.jsx)("strong",{children:"Teacher History"})}),(0,o.jsx)(c.sl,{children:(0,o.jsxs)(c.Sx,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,o.jsx)(c.V,{color:"light",children:(0,o.jsxs)(c.T6,{children:[(0,o.jsx)(c.is,{children:"Name"}),(0,o.jsx)(c.is,{children:"E-mail"}),(0,o.jsx)(c.is,{children:"Mobile No"})]})}),(0,o.jsx)(c.NR,{children:p.map(((e,s)=>(0,o.jsxs)(c.T6,{"v-for":"item in tableItems",children:[(0,o.jsx)(c.NN,{children:(0,o.jsx)("div",{children:e.profile.name.charAt(0)+e.profile.name.slice(1)})}),(0,o.jsx)(c.NN,{children:(0,o.jsx)("div",{children:e.profile.email})}),(0,o.jsx)(c.NN,{children:(0,o.jsx)("div",{children:e.profile.ph_no})})]},s)))})]})})]})})}),b?(0,o.jsx)(h,{visible:j,setVisible:m,SelectedTeacher:b}):null]})}},8682:()=>{}}]);
//# sourceMappingURL=962.69fd144b.chunk.js.map