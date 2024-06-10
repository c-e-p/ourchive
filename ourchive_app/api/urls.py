from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from api import views
from rest_framework.schemas import get_schema_view
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.api_root),
    path('works/', views.WorkList.as_view(), name='work-list'),
    path('works/recent/', views.RecentWorksList.as_view(), name='recent-works-list'),
    path('works/<int:pk>/', views.WorkDetail.as_view(), name='work-detail'),
    path('works/<int:pk>/export/', views.ExportWork.as_view(), name='export-work'),
    path('works/<int:pk>/publish-full/', views.PublishWork.as_view(), name='publish-work'),
    path('works/<int:pk>/draft', views.WorkDraftDetail.as_view(), name='work-draft-detail'),
    path('tags/<int:pk>/works', views.WorkByTagList.as_view(), name='work-by-tags'),
    path('tags/<int:pk>/bookmarks', views.BookmarkByTagList.as_view(), name='bookmark-by-tags'),
    path('chapters/', views.ChapterList.as_view(), name='chapter-list'),
    path('chapters/<int:pk>/', views.ChapterDetail.as_view(), name='chapter-detail'),
    path('chapters/<int:pk>/draft', views.ChapterDraftDetail.as_view(),
         name='chapter-draft-detail'),
    path('works/<int:work_id>/chapters/all',
         views.WorkChapterDetailAll.as_view(), name='work-chapter-detail-all'),
    path('works/<int:work_id>/chapters/',
         views.WorkChapterDetail.as_view(), name='work-chapter-detail'),
    path('chapters/<int:pk>/comments/',
         views.ChapterCommentDetail.as_view(), name='chaptercomment-detail'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('registration-utils/', views.RegistrationUtils.as_view(), name='registration-utils'),
    path('tagtypes/', views.TagTypeList.as_view(), name='tag-type-list'),
    path('tagtypes/<int:pk>/', views.TagTypeDetail.as_view(), name='tagtype-detail'),
    path('tagtypes/browsable/', views.BrowsableTagType.as_view(), name='browsable-tag-type-list'),
    path('tagtypes/browsable/tags', views.TagsByType.as_view(), name='tags-by-type'),
    path('worktypes/', views.WorkTypeList.as_view(), name='work-type-list'),
    path('worktypes/<int:pk>/', views.WorkTypeDetail.as_view(), name='worktype-detail'),
    path('worktypes/<int:type_id>/works',
         views.WorkByTypeList.as_view(), name='work-by-type-list'),
    path('tags/', views.TagList.as_view(), name='tag-list'),
    path('tags/top/', views.TopTagList.as_view(), name='top-tag-list'),
    path('tags/<int:pk>/', views.TagDetail.as_view(), name='tag-detail'),
    path('bookmarks/', views.BookmarkList.as_view(), name='bookmark-list'),
    path('bookmarks/<int:pk>/', views.BookmarkDetail.as_view(), name='bookmark-detail'),
    path('bookmarks/<int:pk>/draft', views.BookmarkDetail.as_view(),
         name='bookmark-draft-detail'),
    path('bookmarks/<int:pk>/comments', views.BookmarkCommentDetail.as_view(),
         name='bookmarkcomment-detail'),
    path('bookmarkcollections/', views.BookmarkCollectionList.as_view(),
         name='bookmark-collection-list'),
    path('bookmarkcollections/<int:pk>/', views.BookmarkCollectionDetail.as_view(),
         name='bookmarkcollection-detail'),
    path('bookmarkcollections/add-work', views.BookmarkCollectionWork.as_view(),
         name='bookmarkcollection-add-work'),
    path('bookmarkcollections/<int:pk>/comments',
         views.BookmarkCollectionCommentDetail.as_view(), name='bookmarkcollectioncomment-detail'),
    path('collectioncomments/', views.CollectionCommentList.as_view(),
         name='collection-comment-list'),
    path('collectioncomments/<int:pk>/', views.CollectionCommentDetail.as_view(),
         name='collectioncomment-detail'),
    path('chaptercomments/', views.CommentList.as_view(), name='comment-list'),
    path('chaptercomments/<int:pk>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('workcomments/<int:pk>/', views.WorkCommentList.as_view(), name='work-comment-list'),
    path('bookmarkcomments/', views.BookmarkCommentList.as_view(),
         name='bookmarkcomment-list'),
    path('bookmarkcomments/<int:pk>/', views.BookmarkPrimaryCommentDetail.as_view(),
         name='bookmarkprimarycomment-detail'),
    path('messages/', views.MessageList.as_view(), name='message-list'),
    path('messages/<int:pk>/', views.MessageDetail.as_view(), name='message-detail'),
    path('notifications/', views.NotificationList.as_view(), name='notification-list'),
    path('notifications/read/', views.NotificationRead.as_view(), name='notification-read'),
    path('notifications/delete-all/', views.NotificationDelete.as_view(), name='notification-delete-all'),
    path('notifications/<int:pk>/', views.NotificationDetail.as_view(),
         name='notification-detail'),
    path('notifications/<int:pk>/read', views.NotificationDetail.as_view(),
         name='notification-read-detail'),
    path('notificationtypes/', views.NotificationTypeList.as_view(),
         name='notification-type-list'),
    path('notificationtypes/<int:pk>/', views.NotificationTypeDetail.as_view(),
         name='notificationtype-detail'),
    path('settings/', views.OurchiveSettingList.as_view(), name='ourchive-setting-list'),
    path('settings/<int:pk>/', views.OurchiveSettingDetail.as_view(),
         name='ourchivesetting-detail'),
    path('settings/', views.OurchiveSettingList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
    path('groups/', views.GroupList.as_view()),
    path('users/import-works/', views.ImportWorks.as_view(), name='import-works'),
    path('users/<int:pk>/importstatus/', views.ImportStatus.as_view(), name='import-status'),
    path('users/profile/<int:pk>', views.UserNameDetail.as_view(), name='user-detail'),
    path('users/export-chives/', views.ExportChives.as_view(), name='export-chives-be'),
    path('users/approvals/', views.UserApprovalList.as_view(), name='user-approvals'),
    path('users/remove-cocreator/', views.UserApprovalRemove.as_view(), name='be-remove-cocreator'),
    path('users/approve-cocreator/', views.UserApprovalApprove.as_view(), name='be-approve-cocreator'),
    path('users/cocreator-bulk-approve/', views.CocreateApproveBulk.as_view(), name='bulk-approve-cocreator'),
    path('users/cocreator-bulk-reject/', views.CocreateRejectBulk.as_view(), name='bulk-reject-cocreator'),
    path('users/<str:username>/works',
         views.UserWorkList.as_view(), name='user-works-drafts'),
    path('users/<str:username>/works/drafts',
         views.UserWorkDraftList.as_view(), name='user-drafts'),
    path('users/<str:username>/bookmarks',
         views.UserBookmarkList.as_view(), name='user-bookmarks'),
    path('users/<str:username>/bookmarkcollections',
         views.UserBookmarkCollectionList.as_view(), name='user-bookmark-collections'),
    path('users/<str:username>/notifications',
         views.UserNotificationList.as_view(), name='user-notifications'),
    path('users/<str:username>/subscriptions',
         views.UserSubscriptionList.as_view(), name='user-subscriptions'),
    path('users/<str:username>/subscriptions/bookmarks',
         views.UserSubscriptionBookmarkList.as_view(), name='user-subscriptions-bookmarks'),
    path('users/<str:username>/subscriptions/collections',
         views.UserSubscriptionBookmarkCollectionList.as_view(), name='user-subscriptions-collections'),
    path('users/<str:username>/subscriptions/works',
         views.UserSubscriptionWorkList.as_view(), name='user-subscriptions-works'),
    path('users/<str:username>/subscriptions/series',
         views.UserSubscriptionSeriesList.as_view(), name='user-subscriptions-series'),
    path('users/<str:username>/subscriptions/anthologies',
         views.UserSubscriptionAnthologyList.as_view(), name='user-subscriptions-anthologies'),
    path('users/<str:username>/bookmarks/drafts',
         views.UserBookmarkDraftList.as_view(), name='user-bookmarks-drafts'),
    path('users/<str:username>/series', views.UserSeriesList.as_view(), name='user-series-list'),
    path('users/<str:username>/anthologies', views.UserAnthologyList.as_view(), name='user-anthologies-list'),
    path('userblocks', views.UserBlocksList.as_view(), name='user-blocks-list'),
    path('userblocks/<int:pk>/', views.UserBlocksDetail.as_view(), name='userblocks-detail'),
    path('userblocks/blocked/<int:user_id>', views.UserBlockSingleDetail.as_view(), name='userblocks-single-detail'),
    path('userreports/', views.UserReportList.as_view(), name='user-report-list'),
    path('userreports/<int:pk>/', views.UserReportDetail.as_view(), name='userreport-detail'),
    path('users/<str:username>/userblocks',
         views.UserBlocksList.as_view(), name='user-blocks-list'),
    path('search/', views.SearchList.as_view(), name='search-list'),
    path('fingerguns/', views.FingergunList.as_view(), name='fingergun-list'),
    path('fingerguns/<int:pk>/', views.FingergunDetail.as_view(), name='fingergun-detail'),
    path('works/<int:work_id>/fingerguns',
         views.FingergunByWorkList.as_view(), name='fingergun-by-work-list'),
    path('tag-autocomplete', views.TagAutocomplete.as_view(), name='tag-autocomplete'),
    path('invitations/', views.Invitations.as_view(), name='invitations'),
    path('attributetypes/', views.AttributeTypeList.as_view(), name='attribute-type-list'),
    path('attributetypes/browsable/', views.BrowsableAttributeType.as_view(), name='browsable-attribute-type'),
    path('attributetypes/browsable/attributes', views.AttributesByType.as_view(), name='attributes-by-type'),
    path('attributetypes/<int:pk>/', views.AttributeTypeDetail.as_view(),
         name='attributetype-detail'),
    path('attributevalues/', views.AttributeValueList.as_view(), name='attribute-value-list'),
    path('attributevalues/<int:pk>/', views.AttributeValueDetail.as_view(),
         name='attributevalue-detail'),
    path('file-upload/', views.FileUpload.as_view(), name='api-file-upload'),
    path('bookmark-autocomplete', views.WorkAutocomplete.as_view(),
         name='bookmark-autocomplete'),
    path('user-autocomplete', views.UserAutocomplete.as_view(),
         name='api-user-autocomplete'),
    path('contentpages/', views.ContentPageList.as_view(), name='content-page-list'),
    path('contentpages/<int:pk>', views.ContentPageDetail.as_view(),
         name='content-page-detail'),
    path('contentpages/mandatory-on-signup/', views.ContentPageMandatoryList.as_view(), name='content-page-mandatory-list'),
    path('reportreasons/', views.ReportReasonList.as_view(), name='report-reasons'),
    path('subscriptions/', views.SubscriptionList.as_view(), name='user-subscriptions'),
    path('subscriptions/<int:pk>/', views.UserSubscriptionDetail.as_view(),
         name='usersubscription-detail'),
    path('adminannouncements/active/', views.AdminAnnouncementActiveList.as_view(),
         name='admin-announcements-active'),
    path('adminannouncements/', views.AdminAnnouncementList.as_view(),
         name='admin-announcements-list'),
    path('adminannouncements/<int:pk>', views.AdminAnnouncementDetail.as_view(),
         name='adminannouncement-detail'),
    path('languages/', views.LanguageList.as_view(), name='language-list'),
    path('news/', views.NewsList.as_view(), name='news-list'),
    path('news/<int:pk>', views.NewsDetail.as_view(), name='news-detail'),
    path('series/', views.SeriesList.as_view(), name='series-list'),
    path('series/<int:pk>/', views.SeriesDetail.as_view(), name='workseries-detail'),
    path('series-autocomplete', views.SeriesAutocomplete.as_view(), name='be-user-autocomplete'),
    path('series/<int:pk>/works', views.WorkSeriesList.as_view(), name='be-series-works'),
    path('series/<int:pk>/work/<int:work_id>', views.WorkSeriesDetail.as_view(), name='be-series-work-detail'),
    path('anthologies/', views.AnthologyList.as_view(), name='anthology-list'),
    path('anthologies/<int:pk>/', views.AnthologyDetail.as_view(), name='anthology-detail'),
    path('anthology-autocomplete', views.AnthologyAutocomplete.as_view(), name='be-anthology-autocomplete'),
    path('anthologies/<int:pk>/works', views.WorkAnthologyList.as_view(), name='be-anthology-works'),
    path('anthologies/<int:pk>/work/<int:work_id>', views.WorkAnthologyDetail.as_view(), name='be-series-anthology-detail'),
    path('openapi', get_schema_view(
        title="Ourchive",
        description="A fan-created archive software package",
        version="1.0.0"
    ), name='openapi-schema'),
    path('redoc/', TemplateView.as_view(
        template_name='redoc.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='redoc'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
