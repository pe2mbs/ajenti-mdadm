// coding=utf-8
// ---------------------------------------------------------------------------
//   MDADM plugin for Ajenti, to manage the MD devices.
//
//   Copyright (C) 2015 Marc Bertens <m.bertens@pe2mbs.nl>
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Affero General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Affero General Public License for more details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see http://www.gnu.org/licenses/agpl-3.0.html.
// ---------------------------------------------------------------------------
//
class window.Controls.mdadm__header extends window.Control
    createDom: () ->
        """
            <div class="control mdadm-header">
                <div class="icon #{@s(@properties.plugin)}">
                    <!-- <img class="image mdadm" src="data:image/png;base64,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"/>
                    -->
                    <div class="mainbar">#{@s(@properties.title)}</div>
                    <div class="bar">#{@s(@properties.plugin)}</div>
                </div>

                <div class="labels">
                    <div class="version">#{@s(@properties.version)}</div>
                    <div class="author">Author: #{@s(@properties.author)}</div>
                    <div class="email">E-Mail: #{@s(@properties.email)}</div>
                </div>

                <div class="inner"><children></div>
            </div>
        """
