from pyramid.config import Configurator
from pkg_resources import resource_filename
from substanced import root_factory
import deform


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings, root_factory=root_factory)
    config.include('substanced')
    config.include('schoolpack.site')
    config.add_catalog_index('title', 'field', 'schoolpack')
    config.add_static_view(
        'sdistatic', 'static', cache_max_age=86400
        )
    config.add_static_view(
        'static', 'retail/static', cache_max_age=86400
        )
    # override deform_bootstrap static registration, it doesn't
    # specify a cache_max_age
    config.add_static_view(
        'static-deform_bootstrap', 'deform_bootstrap:static',
        cache_max_age=86400
        )
    config.scan()
    return config.make_wsgi_app()
    return config.make_wsgi_app()

# set up deform template rendering search path
deform_dir = resource_filename('deform', 'templates')
deform_bootstrap_dir = resource_filename('deform_bootstrap', 'templates')
schoolpack_dir = resource_filename('schoolpack', 'widget/templates')
search_path = (schoolpack_dir, deform_bootstrap_dir, deform_dir)
deform.Form.set_zpt_renderer(search_path)
