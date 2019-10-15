import 'bootstrap';

import '../scss/blogsley.scss';
import { library, dom } from "@fortawesome/fontawesome-svg-core";
/*
import { faSearch, faUserCircle} from "@fortawesome/free-solid-svg-icons";
import { faGithub } from "@fortawesome/free-brands-svg-icons";
library.add(faSearch, faUserCircle, faGithub);
*/
import { fas } from '@fortawesome/free-solid-svg-icons'
import { far } from '@fortawesome/free-regular-svg-icons'
import { fab } from '@fortawesome/free-brands-svg-icons'

// Add all icons to the library so you can use it in your page
library.add(fas, far, fab)

dom.watch();