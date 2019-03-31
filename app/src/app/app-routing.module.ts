import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

const routes: Routes = [
  { path: '', redirectTo: 'tutorial', pathMatch: 'full' },
  { path: 'register', loadChildren: './register/register.module#RegisterPageModule' },
  { path: 'login', loadChildren: './login/login.module#LoginPageModule' },
  { path: 'preferences', loadChildren: './preferences/preferences.module#PreferencesPageModule' },
  { path: 'mode', loadChildren: './mode/mode.module#ModePageModule' },
  { path: 'main', loadChildren: './main/main.module#MainPageModule' },
  { path: 'learn', loadChildren: './learn/learn.module#LearnPageModule' },
  { path: 'test', loadChildren: './test/test.module#TestPageModule' },
  { path: 'tutorial', loadChildren: './tutorial/tutorial.module#TutorialPageModule' },
  { path: 'learn-end', loadChildren: './learn-end/learn-end.module#LearnEndPageModule' },
  { path: 'statistics', loadChildren: './statistics/statistics.module#StatisticsPageModule' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
