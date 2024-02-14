"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[9338,3255,4085,8386,9979],{9979:(e,s,t)=>{t.r(s),t.d(s,{default:()=>l});var r=t(2791),a=t(2585),n=t(2937),i=(t(8682),t(184));const l=e=>{const{state:s,dispatch:t}=(0,r.useContext)(a.y),{objectCount:l,profileDetails:c}=s,{currentStep:o,chageSteps:d}=e;return(0,i.jsx)(i.Fragment,{children:(0,i.jsx)(n.rb,{className:"mb-2",children:(0,i.jsx)(n.b7,{xl:!0,children:(0,i.jsx)(n.xH,{children:(0,i.jsxs)(n.sl,{style:{display:"flex",justifyContent:"space-between"},children:[(0,i.jsx)("nav",{"aria-label":"breadcrumb",children:(0,i.jsxs)("ol",{className:"breadcrumb d-flex align-items-center",style:{margin:"0"},children:[(0,i.jsx)("li",{className:"breadcrumb-item active","aria-current":"page",children:(0,i.jsx)("svg",{style:{marginTop:"-3"},xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-house",viewBox:"0 0 16 16",children:(0,i.jsx)("path",{d:"M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.707 1.5ZM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5 5 5Z"})})}),{term:["term"],semester:["term","semester"],division:["term","semester","division"],batch:["term","semester","division","batch"]}[o].map(((e,s)=>(0,i.jsx)("li",{className:"breadcrumb-item active","aria-current":"page",children:(0,i.jsx)("a",{onClick:()=>{d(e)},className:e===o?"disabled":"",children:e})},s)))]})}),(0,i.jsxs)("span",{children:["Branch - ",c.obj.branch.branch_name]})]})})})})})}},9338:(e,s,t)=>{t.r(s),t.d(s,{default:()=>b});var r=t(2791),a=t(2937),n=t(5294),i=t(8379),l=t(3255),c=t(4085),o=t(8386),d=t(2585),h=t(3645),x=t(9979),m=t(9792),u=t(7689),j=t(184);const g=(e,s)=>{const{state:t,dispatch:i}=(0,r.useContext)(d.y),{accessToken:l,refreshToken:c,batches:o,currentBatch:x,objectCount:g}=t,[p,b]=(0,r.useState)(!1),v=(new Date).getFullYear(),[f,y]=(0,r.useState)(""),[S,C]=(0,r.useState)(v),k=(parseInt(S,10)+1).toString(),[_,w]=((0,u.s0)(),(0,m.Z)());return(0,j.jsx)(j.Fragment,{children:(0,j.jsxs)(a.lx,{className:"row g-3 needs-validation",noValidate:!0,validated:p,onSubmit:t=>{const r=t.currentTarget;t.preventDefault(),!1===r.checkValidity()&&(t.preventDefault(),t.stopPropagation()),b(!0);(async t=>{const r=n.Z.create();let a={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},l=await w(_,r,"/manage/add_term/","post",a,t,null);if(0==l.error){let t=l.response,r={...g};r.terms+=1,i({type:"GET_OBJECTS",payload:r}),e((e=>[...e,t.data.data])),s((e=>e+1)),(0,h.w)("success","Bactch Added successfully...!")}else alert(l.errorMessage.message)})({start_year:S,end_year:k})},children:[(0,j.jsxs)(a.b7,{md:6,children:[(0,j.jsx)(a.L8,{htmlFor:"validationCustom01",children:"Start Year"}),(0,j.jsx)(a.jO,{type:"number",min:v,max:"2099",step:"1",value:S,id:"validationCustom01",onChange:e=>C(e.target.value),required:!0,maxLength:4}),(0,j.jsx)(a.CO,{valid:!0,children:"Looks good!"})]}),(0,j.jsxs)(a.b7,{md:6,children:[(0,j.jsx)(a.L8,{htmlFor:"validationCustom02",children:"End Year"}),(0,j.jsx)(a.jO,{type:"number",value:k,readOnly:!0,step:"1",id:"validationCustom02",required:!0,maxLength:4}),(0,j.jsx)(a.CO,{valid:!0,children:"Looks good!"})]}),(0,j.jsx)(a.b7,{xs:12,children:(0,j.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})})},p=e=>{const{chageSteps:s}=e,{set_term_slug:t}=e,{setBatchCout:i}=e,{state:l,dispatch:c}=(0,r.useContext)(d.y),{accessToken:o,refreshToken:h,batches:x,currentBatch:p}=l,[b,v]=((0,u.s0)(),(0,r.useState)([])),[f,y]=(0,m.Z)(),[S,C]=(0,r.useState)([]);return(0,r.useEffect)((()=>{(async()=>{const e=n.Z.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await y(f,e,"/manage/get_terms","get",s);if(0==t.error){let e=t.response;C(e.data.data)}else alert(t.errorMessage.message)})()}),[]),(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(a.rb,{children:(0,j.jsx)(a.b7,{xs:12,children:(0,j.jsxs)(a.xH,{className:"mb-3",children:[(0,j.jsx)(a.bn,{children:(0,j.jsx)("strong",{children:"Semesters"})}),(0,j.jsx)(a.sl,{children:g(C,i)})]})})}),(0,j.jsx)(a.rb,{children:(0,j.jsx)(a.b7,{xs:!0,children:(0,j.jsxs)(a.xH,{className:"mb-4",children:[(0,j.jsx)(a.bn,{children:(0,j.jsx)("strong",{children:"Term History"})}),(0,j.jsx)(a.sl,{children:S.length>0?(0,j.jsxs)(a.Sx,{align:"middle",className:"mb-0 border text-center",hover:!0,responsive:!0,children:[(0,j.jsx)(a.V,{color:"light",children:(0,j.jsxs)(a.T6,{children:[(0,j.jsx)(a.is,{children:"Start Year"}),(0,j.jsx)(a.is,{children:"End Year"})]})}),(0,j.jsx)(a.NR,{children:S.map(((e,r)=>(0,j.jsxs)(a.T6,{"v-for":"item in tableItems",onClick:()=>{s("semester"),t(e.slug)},children:[(0,j.jsx)(a.NN,{children:(0,j.jsx)("div",{children:e.start_year})}),(0,j.jsx)(a.NN,{children:(0,j.jsx)("div",{children:e.end_year})})]},r)))})]}):(0,j.jsx)("p",{children:"no terms"})})]})})})]})},b=()=>{const[e,s]=(0,r.useState)("term"),[t,h]=(0,r.useState)(""),[u,g]=(0,r.useState)(""),[b,v]=(0,r.useState)(""),[f,y]=(0,r.useState)(0),[S,C]=(0,r.useState)(0),[k,_]=(0,r.useState)(0),{state:w,dispatch:N}=(0,r.useContext)(d.y),{accessToken:T,refreshToken:B,profileDetails:L,objectCount:Z}=w,[V,D]=(0,r.useState)(""),[E,F]=(0,m.Z)(),[O,H]=(0,r.useState)("");(0,r.useEffect)((()=>{"admin"===L.obj.profile.role&&M()}),[]);const M=async()=>{const e=n.Z.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await F(E,e,"/manage/get_object_counts","get",s);if(0==t.error){let e=t.response;N({type:"GET_OBJECTS",payload:e.data})}else alert(t.errorMessage.message)},A=e=>{s(e)},q=[{title:"Terms",value:Z.terms,nextStep:"semester"},{title:"Semester",value:Z.semesters,nextStep:"semester"},{title:"divison",value:Z.divisons,nextStep:"subject"},{title:"Batches",value:Z.batches,nextStep:"batch"}];return(0,j.jsxs)(j.Fragment,{children:[(0,j.jsx)(x.default,{currentStep:e,chageSteps:A}),(0,j.jsx)(i.Z,{}),(0,j.jsx)(a.xH,{className:"mb-4",children:(0,j.jsx)(a.Bt,{children:(0,j.jsx)(a.rb,{xs:{cols:1},md:{cols:4},className:"text-center",children:q.map(((e,s)=>(0,j.jsx)(a.b7,{className:"mb-sm-2 mb-0",children:(0,j.jsxs)(a.u5,{style:{backgroundColor:"transparent",border:"none"},children:[(0,j.jsx)("div",{className:"text-medium-emphasis",children:e.title}),(0,j.jsxs)("strong",{style:{color:"black"},children:[e.value," ",e.percent]})]})},s)))})})}),(()=>{switch(e){case"term":return(0,j.jsx)(p,{chageSteps:A,set_term_slug:H,setBatchCout:y});case"semester":return(0,j.jsx)(o.default,{chageSteps:A,term_slug:O,set_semester_slug:h,setBatchCout:y});case"division":return(0,j.jsx)(l.default,{chageSteps:A,semester_slug:t,set_division_slug:D});case"batch":return(0,j.jsx)(c.default,{chageSteps:A,division_slug:V,setsubSlug:v})}})()]})}},3255:(e,s,t)=>{t.r(s),t.d(s,{default:()=>x});var r=t(2791),a=t(5294),n=t(2585),i=t(2937),l=t(3645),c=t(7689),o=t(9792),d=t(184);const h=(e,s)=>{const[t,h]=(0,o.Z)(),[x,m]=(0,r.useState)(!1),[u,j]=(0,r.useState)(""),{state:g,dispatch:p}=(0,r.useContext)(n.y),{accessToken:b,refreshToken:v,semesters:f,objectCount:y}=g,[S,C]=(0,r.useState)(y);(0,c.s0)();return(0,d.jsxs)(i.lx,{className:"row g-3 needs-validation",noValidate:!0,validated:x,onSubmit:r=>{!1===r.currentTarget.checkValidity()&&(r.preventDefault(),r.stopPropagation()),r.preventDefault(),m(!0);(async s=>{const r=a.Z.create();let n={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},i=await h(t,r,"/manage/add_division/","post",n,s,null);if(0==i.error){let s=i.response;({...y}).divison+=1,e((e=>[...e,s.data.data])),(0,l.w)("success","Semester Added successfully...!")}else alert(i.errorMessage.message)})({division_name:u,semester_slug:s})},children:[(0,d.jsxs)(i.b7,{md:12,children:[(0,d.jsx)(i.L8,{htmlFor:"validationCustom01",children:"Division Name"}),(0,d.jsx)(i.jO,{type:"text",id:"validationCustom01",onChange:e=>j(e.target.value),required:!0}),(0,d.jsx)(i.CO,{valid:!0,children:"Looks good!"})]}),(0,d.jsx)(i.b7,{xs:12,children:(0,d.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},x=e=>{const{semester_slug:s,chageSteps:t,set_division_slug:o}=e,[x,m]=(0,r.useState)([]),{state:u,dispatch:j}=(0,r.useContext)(n.y),{accessToken:g,refreshToken:p,semesters:b}=u;(0,c.s0)();return(0,r.useEffect)((()=>{(async()=>{const e=a.Z.create();let t={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},r=await(0,l.J)(e,"/manage/get_divisions","get",t,null,{semester_slug:s});if(0==r.error){let e=r.response;m(e.data.data)}else alert(r.errorMessage.message)})()}),[]),(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(i.rb,{children:(0,d.jsx)(i.b7,{xs:12,children:(0,d.jsxs)(i.xH,{className:"mb-3",children:[(0,d.jsx)(i.bn,{children:(0,d.jsx)("strong",{children:"Divison"})}),(0,d.jsx)(i.sl,{children:h(m,s)})]})})}),(0,d.jsx)(i.rb,{children:(0,d.jsx)(i.b7,{xs:!0,children:(0,d.jsxs)(i.xH,{className:"mb-4",children:[(0,d.jsx)(i.bn,{children:(0,d.jsx)("strong",{children:"Division History"})}),(0,d.jsx)(i.sl,{children:(0,d.jsxs)(i.Sx,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,d.jsx)(i.V,{color:"light",children:(0,d.jsx)(i.T6,{onClick:()=>{t("batch")},style:{textAlign:"center"},children:(0,d.jsx)(i.is,{children:"Division Name"})})}),(0,d.jsx)(i.NR,{style:{textAlign:"center"},children:x.map(((e,s)=>(0,d.jsx)(i.T6,{onClick:()=>{t("batch"),o(e.slug)},children:(0,d.jsx)(i.NN,{children:(0,d.jsx)("div",{children:e.division_name})})},s)))})]})})]})})})]})}},4085:(e,s,t)=>{t.r(s),t.d(s,{default:()=>j});var r=t(2791),a=t(2007),n=t.n(a),i=t(2585),l=t(5294),c=t(3645),o=t(2937),d=t(7689),h=(t(9434),t(9792)),x=t(184);const m=(e,s)=>{const[t,a]=(0,r.useState)(!1),[n,m]=(0,r.useState)(""),{state:u,dispatch:j}=(0,r.useContext)(i.y),{accessToken:g,refreshToken:p,objectCount:b}=u,[v,f]=((0,d.s0)(),(0,h.Z)());return(0,x.jsxs)(o.lx,{className:"row g-3 needs-validation",noValidate:!0,validated:t,onSubmit:t=>{!1===t.currentTarget.checkValidity()&&(t.preventDefault(),t.stopPropagation()),a(!0);const r={division_slug:e,batch_name:n};t.preventDefault(),(async e=>{const t=l.Z.create();let r={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},a=await f(v,t,"/manage/add_batch/","post",r,e,null);if(0==a.error){let e=a.response,t={...b};t.Batches+=1,j({type:"GET_OBJECTS",payload:t}),s((s=>[...s,e.data.data])),(0,c.w)("success","Batch Added successfully...!")}else alert(a.errorMessage.message)})(r)},children:[(0,x.jsxs)(o.b7,{md:12,children:[(0,x.jsx)(o.L8,{htmlFor:"validationCustom01",children:"Batch Name"}),(0,x.jsx)(o.jO,{type:"text",id:"validationCustom01",onChange:e=>m(e.target.value),required:!0}),(0,x.jsx)(o.CO,{valid:!0,children:"Looks good!"})]}),(0,x.jsx)(o.b7,{xs:12,children:(0,x.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},u=e=>{const[s,t]=(0,h.Z)(),{state:a,dispatch:n}=(0,r.useContext)(i.y),{accessToken:u,refreshToken:j,semesters:g}=a,{division_slug:p,chageSteps:b}=((0,d.s0)(),e),[v,f]=(0,r.useState)([]);return(0,r.useEffect)((()=>{(async()=>{const e=l.Z.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await(0,c.J)(e,"/manage/get_batches","get",s,null,{division_slug:p});if(0==t.error){let e=t.response;f(e.data.data)}else alert(t.errorMessage.message)})()}),[]),(0,x.jsxs)(x.Fragment,{children:[(0,x.jsx)(o.rb,{children:(0,x.jsx)(o.b7,{xs:12,children:(0,x.jsxs)(o.xH,{className:"mb-3",children:[(0,x.jsx)(o.bn,{children:(0,x.jsx)("strong",{children:"Batches"})}),(0,x.jsx)(o.sl,{children:m(p,f)})]})})}),(0,x.jsx)(o.rb,{children:(0,x.jsx)(o.b7,{xs:!0,children:(0,x.jsxs)(o.xH,{className:"mb-4",children:[(0,x.jsx)(o.bn,{children:(0,x.jsx)("strong",{children:"Batch History"})}),(0,x.jsx)(o.sl,{children:(0,x.jsxs)(o.Sx,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,x.jsx)(o.V,{color:"light",children:(0,x.jsx)(o.T6,{className:"text-center",children:(0,x.jsx)(o.is,{children:"Batch Name"})})}),(0,x.jsx)(o.NR,{children:v.map(((e,s)=>(0,x.jsx)(o.T6,{"v-for":"item in tableItems",children:(0,x.jsx)(o.NN,{children:(0,x.jsxs)("div",{className:"text-center",children:[e.division.division_name," | ",e.batch_name]})})},s)))})]})})]})})})]})};u.prototype={chageSteps:n().func.isRequired,semSlug:n().string};const j=u},8386:(e,s,t)=>{t.r(s),t.d(s,{default:()=>x});var r=t(2791),a=t(5294),n=t(7689),i=t(3645),l=t(9792),c=t(2937),o=t(2585),d=t(184);const h=(e,s,t)=>{const{state:h,dispatch:x}=(0,r.useContext)(o.y),{accessToken:m,refreshToken:u,batches:j,currentBatch:g,objectCount:p}=h,[b,v]=(0,r.useState)(!1),f=(new Date).getFullYear(),[y,S]=(0,r.useState)(""),[C,k]=(0,r.useState)(f),[_,w]=((parseInt(C,10)+1).toString(),(0,n.s0)(),(0,l.Z)());return(0,d.jsx)(d.Fragment,{children:(0,d.jsxs)(c.lx,{className:"row g-3 needs-validation",noValidate:!0,validated:b,onSubmit:r=>{const n=r.currentTarget;r.preventDefault(),!1===n.checkValidity()&&(r.preventDefault(),r.stopPropagation()),v(!0);(async t=>{const r=a.Z.create();let n={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},i=await w(_,r,"/manage/add_semester/","post",n,t,null);if(0==i.error){let t=i.response,r={...p};r.semesters+=1,x({type:"GET_OBJECTS",payload:r}),e((e=>[...e,t.data.data])),s((e=>e+1))}else alert(i.errorMessage.message)})({term_slug:t,no:y}),(0,i.w)("success","Bactch Added successfully...!")},children:[(0,d.jsxs)(c.b7,{md:12,children:[(0,d.jsx)(c.L8,{htmlFor:"validationCustom01",children:"Semester Number"}),(0,d.jsx)(c.jO,{type:"number",min:1,max:8,step:"1",id:"validationCustom01",onChange:e=>S(e.target.value),required:!0,maxLength:1}),(0,d.jsx)(c.CO,{valid:!0,children:"Looks good!"})]}),(0,d.jsx)(c.b7,{xs:12,children:(0,d.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})})},x=e=>{const{chageSteps:s}=e,{set_semester_slug:t}=e,{setBatchCout:i}=e,{term_slug:x}=e,{state:m,dispatch:u}=(0,r.useContext)(o.y),{accessToken:j,refreshToken:g,batches:p,currentBatch:b}=m,[v,f]=((0,n.s0)(),(0,r.useState)([])),[y,S]=(0,l.Z)();return(0,r.useEffect)((()=>{j&&(async()=>{const e=a.Z.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await S(y,e,"/manage/get_semesters","get",s,null,{term_slug:x});if(0==t.error){let e=t.response;f(e.data.data)}else alert(t.errorMessage.message)})()}),[]),(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(c.rb,{children:(0,d.jsx)(c.b7,{xs:12,children:(0,d.jsxs)(c.xH,{className:"mb-3",children:[(0,d.jsx)(c.bn,{children:(0,d.jsx)("strong",{children:"Semesters"})}),(0,d.jsx)(c.sl,{children:h(f,i,x)})]})})}),(0,d.jsx)(c.rb,{children:(0,d.jsx)(c.b7,{xs:!0,children:(0,d.jsxs)(c.xH,{className:"mb-4",children:[(0,d.jsx)(c.bn,{children:(0,d.jsx)("strong",{children:"Semester History"})}),(0,d.jsx)(c.sl,{children:(0,d.jsxs)(c.Sx,{align:"middle",className:"mb-0 border text-center",hover:!0,responsive:!0,children:[(0,d.jsx)(c.V,{color:"light",children:(0,d.jsxs)(c.T6,{children:[(0,d.jsx)(c.is,{children:"Semester No"}),(0,d.jsx)(c.is,{children:"Activation Status"})]})}),(0,d.jsx)(c.NR,{children:v.map(((e,r)=>(0,d.jsxs)(c.T6,{"v-for":"item in tableItems",onClick:()=>{s("division"),t(e.slug)},children:[(0,d.jsx)(c.NN,{children:(0,d.jsx)("div",{children:e.no})}),(0,d.jsx)(c.NN,{children:(0,d.jsx)("div",{children:e.status?(0,d.jsx)("div",{children:(0,d.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-check-circle-fill",viewBox:"0 0 16 16",children:(0,d.jsx)("path",{d:"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"})})}):(0,d.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-x-circle-fill",viewBox:"0 0 16 16",children:(0,d.jsx)("path",{d:"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"})})})})]},r)))})]})})]})})})]})}},8379:(e,s,t)=>{t.d(s,{Z:()=>n});t(2791);var r=t(2937),a=t(184);const n=()=>(0,a.jsx)(r.rb,{})},8682:()=>{}}]);
//# sourceMappingURL=9338.717f1f4e.chunk.js.map