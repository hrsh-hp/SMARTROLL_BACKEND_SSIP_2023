# schema.py
import graphene
from graphene_django.types import DjangoObjectType
from .models import Batch, Branch, College, Semester

class BatchType(DjangoObjectType):
    class Meta:
        model = Batch        

class BranchType(DjangoObjectType):
    class Meta:
        model = Branch    
    batches = graphene.List(BatchType, active=graphene.Boolean())

    def resolve_batches(self, info, active=None, **kwargs):        
        if active:
            batches = self.batches.filter(active=True)
            return batches

class CollegeType(DjangoObjectType):
    class Meta:
        model = College

class SemesterType(DjangoObjectType):
    class Meta:
        model = Semester

class CreateBranchMutation(graphene.Mutation):    
    class Arguments:
        branch_name = graphene.String(required=True)
        branch_code = graphene.Int(required=True)

    branch = graphene.Field(BranchType)

    def mutate(self,info,branch_name,branch_code):
        branch = Branch(branch_name=branch_name,branch_code=branch_code)        
        branch.save()
        return CreateBranchMutation(branch=branch)

class Query(graphene.ObjectType):
    all_batches = graphene.List(BatchType)
    all_branches = graphene.List(BranchType)
    all_semesters = graphene.List(SemesterType)    
    branch_by_slug = graphene.Field(BranchType, slug=graphene.String(required=True))
    batch_by_slug = graphene.Field(BatchType,slug=graphene.String(required=True))

    def resolve_all_semesters(self, info, **kwargs):
        return Semester.objects.all()
    
    def resolve_all_batches(self, info, **kwargs):
        return Batch.objects.all()

    def resolve_all_branches(self, info, **kwargs):
        return Branch.objects.all()

    def resolve_branch_by_slug(self, info, slug):
        return Branch.objects.get(slug=slug)
    
    def resolve_batch_by_slug(self,info,slug):
        return Batch.objects.get(slug=slug)
    
class Mutation(graphene.ObjectType):
    createBranch = CreateBranchMutation.Field()

schema = graphene.Schema(query=Query,mutation=Mutation)