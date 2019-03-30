import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LearnEndPage } from './learn-end.page';

describe('LearnEndPage', () => {
  let component: LearnEndPage;
  let fixture: ComponentFixture<LearnEndPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LearnEndPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LearnEndPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
