from rest_framework import renderers


class LowdownJSONRenderer(renderers.JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response_data = {}
        # Name the object list
        object_list = 'data'
        try:
            meta_dict = getattr(renderer_context.get('view').get_serializer().Meta, 'meta_dict')
        except:
            meta_dict = dict()
        try:
            data.get('paginated_results')
            response_data['meta'] = data['meta']
            response_data[object_list] = data['results']
        except:
            response_data[object_list] = data
            response_data['meta'] = dict()
            # Add custom meta data
            response_data['meta'].update(meta_dict)
            # Call super to render the response
            response = super(LowdownJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
        return response
