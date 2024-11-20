// icons
// import {
//   QuestionOutlined,
//   DashboardOutlined,
//   ChromeOutlined,
//   LoginOutlined,
//   ProfileOutlined,
//   FontSizeOutlined,
//   BgColorsOutlined,
//   BarcodeOutlined,
//   CrownOutlined
// } from '@ant-design/icons-vue';

export interface menu {
  header?: string;
  title?: string;
  icon?: string;
  to?: string;
  divider?: boolean;
  chip?: string;
  chipColor?: string;
  chipVariant?: string;
  chipIcon?: string;
  children?: menu[];
  disabled?: boolean;
  type?: string;
  subCaption?: string;
}

const sidebarItem: menu[] = [
  { header: 'Navigation' },
  {
    title: 'Dashboard',
    icon: "mdi-eye",
    to: '/dashboard'
  },
  { header: 'Authentication' },
  {
    title: 'Login',
    icon: "mdi-eye",
    to: '/auth/login'
  },
  {
    title: 'Register',
    icon: "mdi-eye",
    to: '/auth/register'
  },
  { header: 'Utilities' },
  {
    title: 'Typography',
    icon: "mdi-eye",
    to: '/typography'
  },
  {
    title: 'Color',
    icon: "mdi-eye",
    to: '/colors'
  },
  {
    title: 'Shadow',
    icon: "mdi-eye",
    to: '/shadow'
  },
  {
    title: 'Ant Icons',
    icon: "mdi-eye",
    to: '/icon/ant'
  },
  { header: 'Support' },
  {
    title: 'Sample Page',
    icon: "mdi-eye",
    to: '/sample-page'
  },
  {
    title: 'Documentation',
    icon: "mdi-eye",
    to: 'https://codedthemes.gitbook.io/mantis-vuetify/',
    type: 'external',
    chip: 'gitbook',
    chipColor: 'secondary',
    chipVariant: 'flat'
  }
];

export default sidebarItem;
