import { TestBed } from '@angular/core/testing';

import { LoloApiProviderService } from './lolo-api-provider.service';

describe('LoloApiProviderService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: LoloApiProviderService = TestBed.get(LoloApiProviderService);
    expect(service).toBeTruthy();
  });
});
