export default {
  items: [
    {
      name: 'Rooms',
      url: '/main-page',
      icon: 'fa-building-o'
    },
    {
      name: 'Rules',
      url: '/ifttt-list',
      icon: 'fa-cubes',
    },
    {
      name: 'Settings',
      icon: 'fa-cubes',
      children: [
            {
              name: 'General',
              url: '/general-settings',
              icon: 'fa-cubes'
            },
            {
              name: 'Actuators',
              url: '/actuators',
              icon: 'fa-cubes'
            },
            {
              name: 'Sensors',
              url: '/sensors',
              icon: 'fa-cubes'
            }
        ]
    }
  ]
};