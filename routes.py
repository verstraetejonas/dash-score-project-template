import importlib
from typing import List

import dash
from dash.dependencies import Input, Output

from components import notfound
from environment import settings
from utils.routing import find_module_names_in_path, walk_package, PathUtil
from components.navigation import sidebar
import time


def _find_layouts_and_init_callbacks(app: dash.Dash):
    page_names: List[PathUtil] = []
    package_structure = walk_package('pages')
    for package in package_structure:
        top_files = find_module_names_in_path(package)
        # pages/<top_files>/layout.py ??
        if 'layout' in top_files:
            # layout exists, so no sublayouts should exist
            layout_path = [*package.pieces, 'layout']
            # current_top_page = PathUtil(layout_path, [])
            if 'callbacks' in top_files:
                # noinspection PyUnresolvedReferences
                cb_path = '.'.join([*package.pieces, 'callbacks'])
                current_top_page = PathUtil(layout_path, [], cb_path)
                # importlib.import_module().callbacks(app)
            else:
                current_top_page = PathUtil(layout_path, [], None)
            page_names.append(current_top_page)
        else:
            layout_path = [*package.pieces]
            current_top_page = PathUtil(layout_path, [], None)
            sub_packages = walk_package(package.fs_path())
            for sub in sub_packages:
                sub.prepend_piece('pages')
                sub_files = find_module_names_in_path(sub)
                # pages/<top_files>/<sub_files>/layout.py ??
                if 'layout' in sub_files:
                    # sub module is a layout module
                    layout_path = [*sub.pieces, 'layout']
                    # page_names.append(PathUtil(layout_path))
                    if 'callbacks' in sub_files:
                        # noinspection PyUnresolvedReferences
                        cb_path = '.'.join([*sub.pieces, 'callbacks'])
                    else:
                        cb_path = None
                    current_top_page.children.append(PathUtil(layout_path, [], cb_path))
            page_names.append(current_top_page)

    return page_names


def setup_routing(app: dash.Dash) -> List[PathUtil]:
    pages = _find_layouts_and_init_callbacks(app)
    # modules = {x.url(): {'module': importlib.import_module(x.mod_path()),
    #                      'path': x} for x in pages}
    modules = {}
    for p in pages:
        if p.is_page():
            modules[p.url()] = {
                'module': importlib.import_module(p.mod_path()), 'path': p, 'is-child': False,
                'callbacks': importlib.import_module(p.callbacks_path) if p.callbacks_path is not None else None,
                'callbacks_ran': False
            }
        for ch in p.children:
            modules[ch.url()] = {
                'module': importlib.import_module(ch.mod_path()), 'path': ch, 'is-child': True, 'parent': p,
                'callbacks': importlib.import_module(ch.callbacks_path) if ch.callbacks_path is not None else None,
                'callbacks_ran': False
            }

    @app.callback(Output("page-content", "children"), Input("url", "pathname"))
    def render_page_content(pathname):
        curr_path = None
        if pathname in modules:
            curr_path = modules[pathname]
        elif settings.DEFAULT_URL in modules:
            curr_path = modules[settings.DEFAULT_URL]

        sections = []
        print(curr_path)
        if curr_path['is-child']:
            sections.append(sidebar(curr_path['parent'].children))
        if curr_path is not None:
            print('setting current layout')
            sections.append(curr_path['module'].layout)
            if curr_path['callbacks'] is not None and curr_path['callbacks_ran'] is False:
                print('Running callbacks for path')
                curr_path['callbacks'].callbacks(app)
                time.sleep(3)
                curr_path['callbacks_ran'] = True
        else:
            sections.append(notfound)

        return dash.html.Div(className='d-flex flex-row', children=sections)

    return pages
