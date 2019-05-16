import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TestedwordsPage } from './testedwords.page';

describe('TestedwordsPage', () => {
  let component: TestedwordsPage;
  let fixture: ComponentFixture<TestedwordsPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TestedwordsPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestedwordsPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
