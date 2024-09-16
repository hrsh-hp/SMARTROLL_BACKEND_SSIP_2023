"use strict";(self.webpackChunk_coreui_coreui_free_react_admin_template=self.webpackChunk_coreui_coreui_free_react_admin_template||[]).push([[669,243,581,794,949],{3949:(e,s,t)=>{t.r(s),t.d(s,{default:()=>l});var r=t(5043),a=t(7128),n=t(3946),i=(t(8132),t(579));const l=e=>{const{state:s,dispatch:t}=(0,r.useContext)(a.i),{objectCount:l,profileDetails:c}=s,{currentStep:o,chageSteps:d}=e;return(0,i.jsx)(i.Fragment,{children:(0,i.jsx)(n.sK,{className:"mb-2",children:(0,i.jsx)(n.UF,{xl:!0,children:(0,i.jsx)(n.E$,{children:(0,i.jsxs)(n.W6,{style:{display:"flex",justifyContent:"space-between",flexDirection:"column"},children:[(0,i.jsx)("nav",{"aria-label":"breadcrumb",children:(0,i.jsxs)("ol",{className:"mb-3 breadcrumb d-flex align-items-center text-sm sm:text-lg",style:{margin:"0"},children:[(0,i.jsx)("li",{className:"breadcrumb-item active","aria-current":"page",children:(0,i.jsx)("svg",{style:{marginTop:"-3"},xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-house",viewBox:"0 0 16 16",children:(0,i.jsx)("path",{d:"M8.707 1.5a1 1 0 0 0-1.414 0L.646 8.146a.5.5 0 0 0 .708.708L2 8.207V13.5A1.5 1.5 0 0 0 3.5 15h9a1.5 1.5 0 0 0 1.5-1.5V8.207l.646.647a.5.5 0 0 0 .708-.708L13 5.793V2.5a.5.5 0 0 0-.5-.5h-1a.5.5 0 0 0-.5.5v1.293L8.707 1.5ZM13 7.207V13.5a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5V7.207l5-5 5 5Z"})})}),{term:["term"],semester:["term","semester"],division:["term","semester","division"],batch:["term","semester","division","batch"]}[o].map(((e,s)=>(0,i.jsx)("li",{className:"breadcrumb-item active","aria-current":"page",children:(0,i.jsx)("a",{style:{cursor:"grab"},onClick:()=>{d(e)},className:e===o?"disabled":"",children:e})},s)))]})}),(0,i.jsxs)("span",{className:"text-sm sm:text-lg",children:["Branch - ",c.obj.branch.branch_name]})]})})})})})}},8669:(e,s,t)=>{t.r(s),t.d(s,{default:()=>p});var r=t(5043),a=t(3946),n=t(6213),i=t(243),l=t(1581),c=t(2794),o=t(7128),d=t(2355),h=t(3949),m=t(9426),u=t(3216),x=t(579);const g=(e,s)=>{const{state:t,dispatch:i}=(0,r.useContext)(o.i),{accessToken:l,refreshToken:c,batches:h,currentBatch:g,objectCount:j}=t,[p,b]=(0,r.useState)(!1),v=(new Date).getFullYear(),[f,y]=(0,r.useState)(""),[S,k]=(0,r.useState)(v),[C,_]=(0,r.useState)("odd"),w=(parseInt(S,10)+1).toString(),[T,N]=((0,u.Zp)(),(0,m.A)());return(0,r.useEffect)((()=>{console.log(C)}),[C]),(0,x.jsx)(x.Fragment,{children:(0,x.jsxs)(a.qI,{className:"row g-3 needs-validation",noValidate:!0,validated:p,onSubmit:t=>{const r=t.currentTarget;t.preventDefault(),!1===r.checkValidity()&&(t.preventDefault(),t.stopPropagation()),b(!0);(async t=>{const r=n.A.create();let a={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},l=await N(T,r,"/manage/add_term/","post",a,t,null);if(0==l.error){let t=l.response,r={...j};r.terms+=1,i({type:"GET_OBJECTS",payload:r}),e((e=>[...e,t.data.data])),s((e=>e+1)),(0,d.S)("success","Bactch Added successfully...!")}else alert(l.errorMessage.message)})({start_year:S,end_year:w,type:C})},children:[(0,x.jsxs)(a.UF,{md:6,children:[(0,x.jsx)(a.A6,{htmlFor:"validationCustom01",children:"Start Year"}),(0,x.jsx)(a.OG,{type:"number",min:v,max:"2099",step:"1",value:S,id:"validationCustom01",onChange:e=>k(e.target.value),required:!0,maxLength:4}),(0,x.jsx)(a.To,{valid:!0,children:"Looks good!"})]}),(0,x.jsxs)(a.UF,{md:6,children:[(0,x.jsx)(a.A6,{htmlFor:"validationCustom02",children:"End Year"}),(0,x.jsx)(a.OG,{type:"number",value:w,readOnly:!0,step:"1",id:"validationCustom02",required:!0,maxLength:4}),(0,x.jsx)(a.To,{valid:!0,children:"Looks good!"})]}),(0,x.jsx)(a.A6,{htmlFor:"validationCustom02",children:"Type"}),(0,x.jsxs)(a.UF,{md:6,className:"flex  items-center gap-4 -mt-1",children:[(0,x.jsxs)("div",{className:"flex items-center",children:[(0,x.jsx)("input",{type:"radio",name:"term-type",value:"odd",defaultChecked:!0,onClick:e=>{_(e.target.value)},className:"w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"}),(0,x.jsx)("label",{className:"ms-2 text-sm font-medium text-gray-400 dark:text-gray-500",children:"Odd"})]}),(0,x.jsxs)("div",{className:"flex items-center",children:[(0,x.jsx)("input",{type:"radio",name:"term-type",value:"even",onClick:e=>{_(e.target.value)},className:"w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"}),(0,x.jsx)("label",{className:"ms-2 text-sm font-medium text-gray-400 dark:text-gray-500",children:"Even"})]}),(0,x.jsx)(a.To,{valid:!0,children:"Looks good!"})]}),(0,x.jsx)(a.UF,{xs:12,children:(0,x.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})})},j=e=>{const{chageSteps:s}=e,{set_term_slug:t}=e,{set_term_count:i}=e,{state:l,dispatch:c}=(0,r.useContext)(o.i),{accessToken:d,refreshToken:h,batches:j,currentBatch:p}=l,[b,v]=((0,u.Zp)(),(0,r.useState)([])),[f,y]=(0,m.A)(),[S,k]=(0,r.useState)([]);return(0,r.useEffect)((()=>{(async()=>{const e=n.A.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await y(f,e,"/manage/get_terms","get",s);if(0==t.error){let e=t.response;k(e.data.data)}else alert(t.errorMessage.message)})()}),[]),(0,x.jsxs)(x.Fragment,{children:[(0,x.jsx)(a.sK,{children:(0,x.jsx)(a.UF,{xs:12,children:(0,x.jsxs)(a.E$,{className:"mb-3",children:[(0,x.jsx)(a.V0,{children:(0,x.jsx)("strong",{children:"Term"})}),(0,x.jsx)(a.W6,{children:g(k,i)})]})})}),(0,x.jsx)(a.sK,{children:(0,x.jsx)(a.UF,{xs:!0,children:(0,x.jsxs)(a.E$,{className:"mb-4",children:[(0,x.jsx)(a.V0,{children:(0,x.jsx)("strong",{children:"Term History"})}),(0,x.jsx)(a.W6,{children:S.length>0?(0,x.jsxs)(a._v,{align:"middle",className:"mb-0 border text-center",hover:!0,responsive:!0,children:[(0,x.jsx)(a.wV,{color:"light",children:(0,x.jsxs)(a.YI,{children:[(0,x.jsx)(a.$s,{children:"Start Year"}),(0,x.jsx)(a.$s,{children:"End Year"}),(0,x.jsx)(a.$s,{children:"Type"}),(0,x.jsx)(a.$s,{children:"Status"})]})}),(0,x.jsx)(a.jS,{children:S.map(((e,r)=>(0,x.jsxs)(a.YI,{"v-for":"item in tableItems",onClick:()=>{s("semester"),t(e.slug)},style:{cursor:"grab"},children:[(0,x.jsx)(a.cC,{children:(0,x.jsx)("div",{children:e.start_year})}),(0,x.jsx)(a.cC,{children:(0,x.jsx)("div",{children:e.end_year})}),(0,x.jsx)(a.cC,{children:(0,x.jsx)("div",{children:e.type})}),(0,x.jsx)(a.cC,{children:(0,x.jsx)("div",{children:e.status?"Active":"Inactive"})})]},r)))})]}):(0,x.jsx)("p",{children:"no Terms"})})]})})})]})},p=()=>{const[e,s]=(0,r.useState)("term"),[t,d]=(0,r.useState)(""),[u,g]=(0,r.useState)(""),[p,b]=(0,r.useState)(""),[v,f]=(0,r.useState)(0),[y,S]=(0,r.useState)(0),[k,C]=(0,r.useState)(0),[_,w]=(0,r.useState)(0),{state:T,dispatch:N}=(0,r.useContext)(o.i),{accessToken:F,refreshToken:A,profileDetails:E,objectCount:V}=T,[B,U]=(0,r.useState)(""),[L,D]=(0,m.A)(),[I,$]=(0,r.useState)("");(0,r.useEffect)((()=>{"admin"===E.obj.profile.role&&M()}),[]);const M=async()=>{const e=n.A.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await D(L,e,"/manage/get_object_counts","get",s);if(0==t.error){let e=t.response;N({type:"GET_OBJECTS",payload:e.data})}else alert(t.errorMessage.message)},Y=e=>{s(e)},O=[{title:"Terms",value:V.terms,nextStep:"semester"},{title:"Semester",value:V.semesters,nextStep:"semester"},{title:"divison",value:V.divisons,nextStep:"subject"},{title:"Batches",value:V.batches,nextStep:"batch"}];return(0,x.jsxs)(x.Fragment,{children:[(0,x.jsx)(h.default,{currentStep:e,chageSteps:Y}),(0,x.jsx)(a.E$,{className:"mb-4",children:(0,x.jsx)(a.XW,{children:(0,x.jsx)(a.sK,{xs:{cols:1},md:{cols:4},className:"text-center",children:O.map(((e,s)=>(0,x.jsx)(a.UF,{className:"mb-sm-2 mb-0",children:(0,x.jsxs)(a.Q_,{style:{backgroundColor:"transparent",border:"none",cursor:"default"},children:[(0,x.jsx)("div",{className:"text-medium-emphasis",children:e.title}),(0,x.jsxs)("strong",{style:{color:"black"},children:[e.value," ",e.percent]})]})},s)))})})}),(()=>{switch(e){case"term":return(0,x.jsx)(j,{chageSteps:Y,set_term_slug:$,set_term_count:f});case"semester":return(0,x.jsx)(c.default,{chageSteps:Y,term_slug:I,set_semester_slug:d,setsemCount:S});case"division":return(0,x.jsx)(i.default,{chageSteps:Y,semester_slug:t,set_division_slug:U,set_divisionCount:C});case"batch":return(0,x.jsx)(l.default,{chageSteps:Y,division_slug:B,setsubSlug:b,setBatchCout:w})}})()]})}},243:(e,s,t)=>{t.r(s),t.d(s,{default:()=>m});var r=t(5043),a=t(6213),n=t(7128),i=t(3946),l=t(2355),c=t(3216),o=t(9426),d=t(579);const h=(e,s,t)=>{const[h,m]=(0,o.A)(),[u,x]=(0,r.useState)(!1),[g,j]=(0,r.useState)(null),{state:p,dispatch:b}=(0,r.useContext)(n.i),{accessToken:v,refreshToken:f,semesters:y,objectCount:S}=p,[k,C]=(0,r.useState)(S);(0,c.Zp)();return(0,d.jsxs)(i.qI,{className:"row g-3 needs-validation",noValidate:!0,validated:u,onSubmit:r=>{!1===r.currentTarget.checkValidity()&&(r.preventDefault(),r.stopPropagation()),r.preventDefault(),x(!0);(async s=>{if(g){const r={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},n=a.A.create();let i="/manage/add_division/",c="post",o=r,d=await m(h,n,i,c,o,s,null);if(0==d.error){let s=d.response,r={...S};r.divisons+=1,b({type:"GET_OBJECTS",payload:r}),e((e=>[...e,s.data.data])),t((e=>e+1)),(0,l.S)("success","Semester Added successfully...!")}else alert(d.errorMessage.message)}else alert("Please Enter The Valid Division Name")})({division_name:g,semester_slug:s})},children:[(0,d.jsxs)(i.UF,{md:12,children:[(0,d.jsx)(i.A6,{htmlFor:"validationCustom01",children:"Division Name"}),(0,d.jsx)(i.OG,{type:"text",id:"validationCustom01",onChange:e=>j(e.target.value.toUpperCase()),required:!0,maxLength:1}),(0,d.jsx)(i.To,{valid:!0,children:"Looks good!"})]}),(0,d.jsx)(i.UF,{xs:12,children:(0,d.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},m=e=>{const{semester_slug:s,chageSteps:t,set_division_slug:o,set_divisionCount:m}=e,[u,x]=(0,r.useState)([]),{state:g,dispatch:j}=(0,r.useContext)(n.i),{accessToken:p,refreshToken:b,semesters:v}=g;(0,c.Zp)();return(0,r.useEffect)((()=>{(async()=>{const e=a.A.create();let t={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},r=await(0,l.R)(e,"/manage/get_divisions","get",t,null,{semester_slug:s});if(0==r.error){let e=r.response;x(e.data.data)}else alert(r.errorMessage.message)})()}),[]),(0,d.jsxs)(d.Fragment,{children:[(0,d.jsx)(i.sK,{children:(0,d.jsx)(i.UF,{xs:12,children:(0,d.jsxs)(i.E$,{className:"mb-3",children:[(0,d.jsx)(i.V0,{children:(0,d.jsx)("strong",{children:"Divison"})}),(0,d.jsx)(i.W6,{children:h(x,s,m)})]})})}),(0,d.jsx)(i.sK,{children:(0,d.jsx)(i.UF,{xs:!0,children:(0,d.jsxs)(i.E$,{className:"mb-4",children:[(0,d.jsx)(i.V0,{children:(0,d.jsx)("strong",{children:"Division History"})}),(0,d.jsx)(i.W6,{children:(0,d.jsxs)(i._v,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,d.jsx)(i.wV,{color:"light",children:(0,d.jsx)(i.YI,{onClick:()=>{t("batch")},style:{textAlign:"center"},children:(0,d.jsx)(i.$s,{children:"Division Name"})})}),(0,d.jsx)(i.jS,{style:{textAlign:"center"},children:u.map(((e,s)=>(0,d.jsx)(i.YI,{onClick:()=>{t("batch"),o(e.slug)},style:{cursor:"pointer"},children:(0,d.jsx)(i.cC,{children:(0,d.jsx)("div",{children:e.division_name})})},s)))})]})})]})})})]})}},1581:(e,s,t)=>{t.r(s),t.d(s,{default:()=>g});var r=t(5043),a=t(5173),n=t.n(a),i=t(7128),l=t(6213),c=t(2355),o=t(3946),d=t(3216),h=(t(9456),t(9426)),m=t(579);const u=(e,s,t)=>{const[a,n]=(0,r.useState)(!1),[u,x]=(0,r.useState)(null),{state:g,dispatch:j}=(0,r.useContext)(i.i),{accessToken:p,refreshToken:b,objectCount:v}=g,[f,y]=((0,d.Zp)(),(0,h.A)());return(0,m.jsxs)(o.qI,{className:"row g-3 needs-validation",noValidate:!0,validated:a,onSubmit:r=>{!1===r.currentTarget.checkValidity()&&(r.preventDefault(),r.stopPropagation()),n(!0);const a={division_slug:e,batch_name:u};r.preventDefault(),(async e=>{u||alert("Please Enter The Valid Batch Name");const r=l.A.create();let a={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},n=await y(f,r,"/manage/add_batch/","post",a,e,null);if(0==n.error){let e=n.response,r={...v};r.batches+=1,j({type:"GET_OBJECTS",payload:r}),s((s=>[...s,e.data.data])),t((e=>e+1)),(0,c.S)("success","Batch Added successfully...!")}else alert(n.errorMessage.message)})(a)},children:[(0,m.jsxs)(o.UF,{md:12,children:[(0,m.jsx)(o.A6,{htmlFor:"validationCustom01",children:"Batch Name"}),(0,m.jsx)(o.OG,{type:"text",id:"validationCustom01",onChange:e=>x(e.target.value),required:!0}),(0,m.jsx)(o.To,{valid:!0,children:"Looks good!"})]}),(0,m.jsx)(o.UF,{xs:12,children:(0,m.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})},x=e=>{const[s,t]=(0,h.A)(),{state:a,dispatch:n}=(0,r.useContext)(i.i),{accessToken:x,refreshToken:g,semesters:j}=a,{division_slug:p,chageSteps:b,setBatchCout:v}=((0,d.Zp)(),e),[f,y]=(0,r.useState)([]);return(0,r.useEffect)((()=>{(async()=>{const e=l.A.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await(0,c.R)(e,"/manage/get_batches","get",s,null,{division_slug:p});if(0==t.error){let e=t.response;y(e.data.data)}else alert(t.errorMessage.message)})()}),[]),(0,m.jsxs)(m.Fragment,{children:[(0,m.jsx)(o.sK,{children:(0,m.jsx)(o.UF,{xs:12,children:(0,m.jsxs)(o.E$,{className:"mb-3",children:[(0,m.jsx)(o.V0,{children:(0,m.jsx)("strong",{children:"Batches"})}),(0,m.jsx)(o.W6,{children:u(p,y,v)})]})})}),(0,m.jsx)(o.sK,{children:(0,m.jsx)(o.UF,{xs:!0,children:(0,m.jsxs)(o.E$,{className:"mb-4",children:[(0,m.jsx)(o.V0,{children:(0,m.jsx)("strong",{children:"Batch History"})}),(0,m.jsx)(o.W6,{children:(0,m.jsxs)(o._v,{align:"middle",className:"mb-0 border",hover:!0,responsive:!0,children:[(0,m.jsx)(o.wV,{color:"light",children:(0,m.jsx)(o.YI,{className:"text-center",children:(0,m.jsx)(o.$s,{children:"Batch Name"})})}),(0,m.jsx)(o.jS,{children:f.map(((e,s)=>(0,m.jsx)(o.YI,{"v-for":"item in tableItems",children:(0,m.jsx)(o.cC,{children:(0,m.jsxs)("div",{className:"text-center",children:[e.division.division_name," | ",e.batch_name]})})},s)))})]})})]})})})]})};x.prototype={chageSteps:n().func.isRequired,semSlug:n().string};const g=x},2794:(e,s,t)=>{t.r(s),t.d(s,{default:()=>h});var r=t(5043),a=t(6213),n=t(3216),i=(t(2355),t(9426)),l=t(3946),c=t(7128),o=t(579);const d=(e,s,t)=>{const{state:d,dispatch:h}=(0,r.useContext)(c.i),{accessToken:m,refreshToken:u,batches:x,currentBatch:g,objectCount:j}=d,[p,b]=(0,r.useState)(!1),v=(new Date).getFullYear(),[f,y]=(0,r.useState)(0),[S,k]=(0,r.useState)(v),[C,_]=((parseInt(S,10)+1).toString(),(0,n.Zp)(),(0,i.A)());return(0,o.jsx)(o.Fragment,{children:(0,o.jsxs)(l.qI,{className:"row g-3 needs-validation",noValidate:!0,validated:p,onSubmit:r=>{const n=r.currentTarget;if(r.preventDefault(),!1===n.checkValidity())return r.preventDefault(),r.stopPropagation(),void alert("Please enter the valid semester details");b(!0);(async t=>{if(0!=f){const r={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},n=a.A.create();let i="/manage/add_semester/",l="post",c=r,o=await _(C,n,i,l,c,t,null);if(0==o.error){let t=o.response,r={...j};r.semesters+=1,h({type:"GET_OBJECTS",payload:r}),e((e=>[...e,t.data.data])),s((e=>e+1))}else alert(o.errorMessage.message)}else alert("Please Enter the Valid Semester Number")})({term_slug:t,no:f})},children:[(0,o.jsxs)(l.UF,{md:12,children:[(0,o.jsx)(l.A6,{htmlFor:"validationCustom01",children:"Semester Number"}),(0,o.jsx)(l.OG,{type:"number",min:1,max:8,step:"1",id:"validationCustom01",onChange:e=>y(e.target.value),required:!0,maxLength:1}),(0,o.jsx)(l.To,{valid:!0,children:"Looks good!"})]}),(0,o.jsx)(l.UF,{xs:12,children:(0,o.jsx)("button",{className:"btn btn-outline-dark form-control",type:"submit",children:"Submit form"})})]})})},h=e=>{const{chageSteps:s}=e,{set_semester_slug:t}=e,{setsemCount:h}=e,{term_slug:m}=e,{state:u,dispatch:x}=(0,r.useContext)(c.i),{accessToken:g,refreshToken:j,batches:p,currentBatch:b}=u,[v,f]=((0,n.Zp)(),(0,r.useState)([])),[y,S]=(0,i.A)();return(0,r.useEffect)((()=>{g&&(async()=>{const e=a.A.create();let s={"Content-Type":"application/json","ngrok-skip-browser-warning":!0},t=await S(y,e,"/manage/get_semesters","get",s,null,{term_slug:m});if(0==t.error){let e=t.response;f(e.data.data)}else alert(t.errorMessage.message)})()}),[]),(0,o.jsxs)(o.Fragment,{children:[(0,o.jsx)(l.sK,{children:(0,o.jsx)(l.UF,{xs:12,children:(0,o.jsxs)(l.E$,{className:"mb-3",children:[(0,o.jsx)(l.V0,{children:(0,o.jsx)("strong",{children:"Semesters"})}),(0,o.jsx)(l.W6,{children:d(f,h,m)})]})})}),(0,o.jsx)(l.sK,{children:(0,o.jsx)(l.UF,{xs:!0,children:(0,o.jsxs)(l.E$,{className:"mb-4",children:[(0,o.jsx)(l.V0,{children:(0,o.jsx)("strong",{children:"Semester History"})}),(0,o.jsx)(l.W6,{children:(0,o.jsxs)(l._v,{align:"middle",className:"mb-0 border text-center",hover:!0,responsive:!0,children:[(0,o.jsx)(l.wV,{color:"light",children:(0,o.jsxs)(l.YI,{children:[(0,o.jsx)(l.$s,{children:"Semester No"}),(0,o.jsx)(l.$s,{children:"Activation Status"})]})}),(0,o.jsx)(l.jS,{children:v.map(((e,r)=>(0,o.jsxs)(l.YI,{"v-for":"item in tableItems",onClick:()=>{s("division"),t(e.slug)},style:{cursor:"grab"},children:[(0,o.jsx)(l.cC,{children:(0,o.jsx)("div",{children:e.no})}),(0,o.jsx)(l.cC,{children:(0,o.jsx)("div",{className:"d-flex justify-content-center",children:e.status?(0,o.jsx)("div",{children:(0,o.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-check-circle-fill",viewBox:"0 0 16 16",children:(0,o.jsx)("path",{d:"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"})})}):(0,o.jsx)("svg",{xmlns:"http://www.w3.org/2000/svg",width:"16",height:"16",fill:"currentColor",className:"bi bi-x-circle-fill",viewBox:"0 0 16 16",children:(0,o.jsx)("path",{d:"M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM5.354 4.646a.5.5 0 1 0-.708.708L7.293 8l-2.647 2.646a.5.5 0 0 0 .708.708L8 8.707l2.646 2.647a.5.5 0 0 0 .708-.708L8.707 8l2.647-2.646a.5.5 0 0 0-.708-.708L8 7.293 5.354 4.646z"})})})})]},r)))})]})})]})})})]})}},8132:()=>{}}]);
//# sourceMappingURL=669.93123a2b.chunk.js.map