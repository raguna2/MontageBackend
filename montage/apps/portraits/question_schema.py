import datetime
import logging
from typing import Any, Dict, List, Optional

from apps.accounts.models import MontageUser
from apps.accounts.schemas import UserType
from apps.categories.models import Category
from apps.portraits.models import Impression, Question
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import F, Prefetch
import graphene
from graphene_django.types import DjangoObjectType

logger = logging.getLogger(__name__)


class QuestionType(DjangoObjectType):
    """QuestionType."""

    class Meta:
        """Meta."""
        model = Question


class FilteredQuestionType(DjangoObjectType):
    """QuestionType."""
    personalized = graphene.Field(QuestionType, source='personalized')
    masters = graphene.Field(QuestionType, source='masters')

    class Meta:
        """Meta."""
        model = Question


class AnswerType(graphene.ObjectType):
    question_id = graphene.Int()
    about = graphene.String()
    category_id = graphene.Int()
    appeared_at = graphene.String()
    updated_at = graphene.String()
    is_personal = graphene.Boolean()
    impression_id = graphene.Int()
    user_id = graphene.Int()
    answer = graphene.String()
    is_target = graphene.Boolean()


class CreateQuestionMutation(graphene.Mutation):
    """
    Questionの作成
    """
    question = graphene.Field(FilteredQuestionType)

    class Arguments:
        about = graphene.String()

    def mutate(self, info, about):
        user_id = info.context.user.id
        try:
            user = MontageUser.objects.get(id=user_id)
        except MontageUser.DoesNotExist as e:
            logger.error(e)
            return None

        # ユーザが作成したものは自動的にmy_questionカテゴリになる
        category = Category.objects.get(name='my_question')
        # ユーザが質問を作る用のMutationなのでis_personalはデフォルト値
        question = Question.objects.create(about=about, category=category)
        # userはmanytomany
        question.user.add(user)
        question.save()
        return CreateQuestionMutation(question=question)


class DeleteQuestionMutation(graphene.Mutation):
    """
    Questionの削除
    """
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.Int()

    def mutate(self, info, id):
        question = Question.objects.filter(id=id)
        try:
            question.delete()
            ok = True
        except ObjectDoesNotExist as e:
            logger.error('存在しないオブジェクトは削除できません')
            logger.error(e)

        return DeleteQuestionMutation(ok=ok)


class Mutation(graphene.ObjectType):
    create_question = CreateQuestionMutation.Field()
    delete_question = DeleteQuestionMutation.Field()


class Query(graphene.ObjectType):
    category_questions = graphene.List(
        FilteredQuestionType,
        user_id=graphene.Int(),
        category_id=graphene.Int(),
        page=graphene.Int(),
        size=graphene.Int(),
    )
    questions = graphene.List(FilteredQuestionType)
    answers_for_individual_page = graphene.List(
        AnswerType,
        target_user_id=graphene.Int(),
        target_impression_id=graphene.Int(),
    )

    def resolve_category_questions(
            self, info, user_id, category_id, page, size):
        """ユーザのカテゴリごとの質問(未回答のみ)

        Parameters
        -----------------
        info: Any
            リクエスト

        user_id: int
            質問を取得するユーザID

        category_id: int
            取得するカテゴリのID

        page: int
            取得開始位置

        size: int
            取得件数

        Notes
        -----------------
        回答のあるImpressionのIDをrev_impressionにもたないQuestionが未回答質問

        """
        # 既に回答のあるもののIDリストを作成
        ids = Impression.objects.filter(
            user__pk=user_id
        ).values_list('id', flat=True)

        # ユーザに紐づく未回答質問のみを抽出
        # TODO: annotateでidsを生成できる
        category_questions = Question.objects.filter(
            category__id=category_id,
        ).exclude(
            rev_impression__id__in=ids,
        ).select_related(
            'category'
        ).prefetch_related(
            Prefetch(
                'rev_impression',
                queryset=Impression.objects.filter(user__pk=user_id)
            )
        )

        start = page * size if page > 0 else 0
        end = size + page * size if page > 0 else size
        return category_questions[start:end]

    def resolve_questions(self, info):
        return Question.objects.all()

    def resolve_answers_for_individual_page(
            self, info, target_user_id: int, target_impression_id: int):
        """個別回答ページで用いる質問と回答を取得する

        Notes
        ----------------------
        targetには個別回答をextraにはその他の回答を入れて返却する

        Examples
        --------------------
        IN
        >>> query{
              answersForIndividualPage(targetUserId: 2, targetImpressionId: 23){
                questionId
                about
                answer
                appearedAt
                updatedAt
                categoryId
                isPersonal
                userId
                impressionId
                isTarget
            }

        OUT
        >>> {
              "data": {
                "answersForIndividualPage": [
                  {
                    "questionId": 4,
                    "about": "初恋はいつ?",
                    "answer": "76767",
                    "appearedAt": "2020-02-29 03:21:36.116495+00:00",
                    "updatedAt": "2020-02-29 03:21:36.116537+00:00",
                    "categoryId": 2,
                    "isPersonal": false,
                    "userId": 2,
                    "impressionId": 23,
                    "isTarget": true
                  },
                  ...
                ]
              }
            }

        """
        question_with_answers = Question.objects.prefetch_related(
            Prefetch(
                'rev_impression',
                queryset=Impression.objects.filter(user_id=target_user_id)
            )
        ).annotate(
            question_id=F('id'),
            impression_id=F('rev_impression__id'),
            user_id=F('rev_impression__user'),
            answer=F('rev_impression__content'),
        ).filter(
            user_id=target_user_id,
            rev_impression__id=target_impression_id
        ).values()

        if not question_with_answers:
            logger.debug("question_with_answers is not found.")
            return []

        results: List[Dict[str, Any]] = []
        for item in question_with_answers:
            is_target = bool(target_impression_id == item['impression_id'])
            answer = AnswerType(
                question_id=item['question_id'],
                about=item['about'],
                category_id=item['category_id'],
                appeared_at=item['appeared_at'],
                updated_at=item['updated_at'],
                is_personal=item['is_personal'],
                impression_id=item['impression_id'],
                user_id=item['user_id'],
                answer=item['answer'],
                is_target=is_target,
            )
            if is_target:
                # 常にtargetは先頭
                results.insert(0, answer)
            else:
                # それ以外は末尾に追加
                results.append(answer)

        return results
